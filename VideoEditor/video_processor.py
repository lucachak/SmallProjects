import cv2
import os
import subprocess
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import tempfile

@dataclass
class TriggerConfig:
    """Configuração para cada imagem de trigger"""
    image_path: str
    threshold: float = 0.8
    name: str = None
    
    def __post_init__(self):
        if self.name is None:
            self.name = os.path.basename(self.image_path)

class VideoProcessor:
    """
    Processador de vídeo inteligente que corta baseado em imagens de trigger
    """
    
    def __init__(self, video_path: str):
        self.video_path = video_path
        self._video_info = None
    
    def get_video_info(self) -> Dict[str, Any]:
        """Obtém informações do vídeo usando ffprobe"""
        if self._video_info is None:
            self._video_info = self._extract_video_info()
        return self._video_info
    
    def _extract_video_info(self) -> Dict[str, Any]:
        """Extrai metadados do vídeo"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json',
                '-show_format', '-show_streams', self.video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            
            info = {
                'filename': os.path.basename(self.video_path),
                'file_size_mb': round(os.path.getsize(self.video_path) / (1024 * 1024), 2)
            }
            
            if 'format' in data:
                format_info = data['format']
                info.update({
                    'duration': float(format_info.get('duration', 0)),
                    'bit_rate': format_info.get('bit_rate'),
                    'format': format_info.get('format_name')
                })
            
            for stream in data.get('streams', []):
                if stream.get('codec_type') == 'video':
                    info.update({
                        'width': stream.get('width'),
                        'height': stream.get('height'),
                        'fps': self._parse_fps(stream.get('r_frame_rate')),
                        'codec': stream.get('codec_name')
                    })
                    break
            
            return info
        except Exception as e:
            return {'error': str(e)}
    
    def _parse_fps(self, fps_str):
        """Converte string de FPS para número"""
        if fps_str and '/' in fps_str:
            try:
                num, den = map(int, fps_str.split('/'))
                return round(num / den, 2) if den != 0 else 0
            except (ValueError, ZeroDivisionError):
                return 0
        return fps_str
    
    def _compare_frames(self, frame1, frame2) -> float:
        """
        Compara duas imagens e retorna similaridade (0-1)
        
        Como funciona:
        1. Redimensiona as imagens para terem o mesmo tamanho
        2. Converte para escala de cinza
        3. Usa template matching para calcular similaridade
        4. Retorna valor entre 0 (diferentes) e 1 (idênticas)
        """
        # Redimensiona para mesmo tamanho
        if frame1.shape != frame2.shape:
            frame2 = cv2.resize(frame2, (frame1.shape[1], frame1.shape[0]))
        
        # Converte para cinza (mais rápido e preciso para comparação)
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        
        # Template Matching - técnica que desliza uma imagem sobre a outra
        # e calcula a correlação em cada posição
        result = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)
        similarity = cv2.minMaxLoc(result)[1]  # Pega o valor máximo de similaridade
        
        return float(similarity)
    
    def find_first_trigger(self, triggers: List[TriggerConfig], 
                          start_time: float = 0) -> Dict[str, Any]:
        """
        Encontra o primeiro trigger que aparece no vídeo
        
        Como funciona:
        1. Abre o vídeo frame por frame
        2. Para cada frame, compara com TODOS os triggers
        3. Retorna no primeiro que passar do threshold
        4. Se nenhum for encontrado, retorna o mais similar
        """
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            return {'success': False, 'error': 'Não foi possível abrir o vídeo'}
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        start_frame = int(start_time * fps)
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        # Carrega todas as imagens de trigger
        trigger_data = []
        for trigger in triggers:
            img = cv2.imread(trigger.image_path)
            if img is not None:
                trigger_data.append({
                    'config': trigger,
                    'image': img,
                    'best_similarity': 0.0,
                    'best_frame': 0
                })
        
        if not trigger_data:
            cap.release()
            return {'success': False, 'error': 'Nenhuma imagem de trigger válida'}
        
        frame_count = start_frame
        best_overall = {'similarity': 0.0, 'trigger': None, 'frame': 0}
        
        print(f"🔍 Procurando {len(trigger_data)} triggers...")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Verifica cada trigger neste frame
            for trigger_info in trigger_data:
                similarity = self._compare_frames(frame, trigger_info['image'])
                
                # Atualiza melhor similaridade para estatísticas
                if similarity > trigger_info['best_similarity']:
                    trigger_info['best_similarity'] = similarity
                    trigger_info['best_frame'] = frame_count
                
                # Verifica se encontrou um trigger
                if similarity >= trigger_info['config'].threshold:
                    timestamp = frame_count / fps
                    cap.release()
                    
                    return {
                        'success': True,
                        'trigger_name': trigger_info['config'].name,
                        'frame_number': frame_count,
                        'timestamp': timestamp,
                        'similarity': similarity,
                        'message': f"Trigger '{trigger_info['config'].name}' encontrado em {timestamp:.2f}s"
                    }
            
            # Atualiza melhor match geral
            current_best = max(trigger_data, key=lambda x: x['best_similarity'])
            if current_best['best_similarity'] > best_overall['similarity']:
                best_overall = {
                    'similarity': current_best['best_similarity'],
                    'trigger': current_best['config'].name,
                    'frame': current_best['best_frame']
                }
            
            frame_count += 1
            
            # Progresso a cada 5%
            if frame_count % (total_frames // 20) == 0:
                progress = (frame_count / total_frames) * 100
                print(f"📊 Progresso: {progress:.1f}%")
        
        cap.release()
        
        # Se chegou aqui, nenhum trigger foi encontrado
        return {
            'success': False,
            'error': f"Nenhum trigger encontrado. Melhor match: {best_overall['trigger']} com {best_overall['similarity']:.3f}",
            'best_match': best_overall
        }
    
    def cut_video_at_trigger(self, triggers: List[TriggerConfig], 
                           output_path: str,
                           cut_mode: str = 'after') -> Dict[str, Any]:
        """
        Corta o vídeo no primeiro trigger encontrado
        
        Args:
            triggers: Lista de configurações de trigger
            output_path: Caminho do arquivo de saída
            cut_mode: 'after' (mantém do início até o trigger) 
                     'before' (mantém do trigger até o fim)
        """
        # Primeiro encontra o trigger
        detection_result = self.find_first_trigger(triggers)
        
        if not detection_result['success']:
            return detection_result
        
        # Configura o corte baseado no modo
        info = self.get_video_info()
        fps = info.get('fps', 30)
        trigger_frame = detection_result['frame_number']
        
        if cut_mode == 'after':
            # Mantém do início até o trigger
            start_time = 0
            end_time = trigger_frame / fps
            duration = end_time
        else:  # before
            # Mantém do trigger até o fim
            start_time = trigger_frame / fps
            duration = None
        
        try:
            # Monta comando ffmpeg
            cmd = ['ffmpeg', '-i', self.video_path]
            
            if start_time > 0:
                cmd.extend(['-ss', str(start_time)])
            
            if duration is not None:
                cmd.extend(['-t', str(duration)])
            
            cmd.extend(['-c', 'copy', '-y', output_path])  # -y sobrescreve
            
            print(f"✂️ Cortando vídeo...")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            return {
                'success': True,
                'output_path': output_path,
                'cut_position': detection_result['timestamp'],
                'trigger_name': detection_result['trigger_name'],
                'similarity': detection_result['similarity'],
                'message': f"Vídeo cortado com sucesso em {detection_result['timestamp']:.2f}s"
            }
            
        except subprocess.CalledProcessError as e:
            return {
                'success': False,
                'error': f"Erro ao cortar vídeo: {e.stderr}"
            }
    
    def process_multiple_videos(self, video_paths: List[str], 
                              triggers: List[TriggerConfig],
                              output_dir: str,
                              cut_mode: str = 'after') -> List[Dict[str, Any]]:
        """Processa múltiplos vídeos em lote"""
        results = []
        
        for i, video_path in enumerate(video_paths):
            print(f"🎬 Processando vídeo {i+1}/{len(video_paths)}: {os.path.basename(video_path)}")
            
            processor = VideoProcessor(video_path)
            output_path = os.path.join(output_dir, f"edited_{os.path.basename(video_path)}")
            
            result = processor.cut_video_at_trigger(triggers, output_path, cut_mode)
            result['video_name'] = os.path.basename(video_path)
            results.append(result)
        
        return results
