import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import subprocess
import os
import threading
import re

class DarkProConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Minimal Audio to MP4 Pro (Dark Mode)")
        self.root.geometry("700x550")
        self.root.configure(bg="#1e1e1e") # 다크모드 배경

        # 스타일 및 변수 설정
        self.setup_styles()
        self.audio_files = [] # 일괄 변환을 위한 파일 리스트
        self.image_path = tk.StringVar()
        self.use_waveform = tk.BooleanVar(value=False)
        self.status_msg = tk.StringVar(value="파일을 아래에 드래그하거나 버튼으로 추가하세요.")
        self.progress_val = tk.DoubleVar(value=0)

        # === UI 레이아웃 ===
        main_frame = ttk.Frame(root, padding="20", style="Dark.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. 헤더
        header = ttk.Label(main_frame, text="AUDIO → MP4 CONVERTER PRO", font=("Arial", 16, "bold"), style="Dark.TLabel")
        header.pack(pady=(0, 20))

        # 2. 오디오 파일 리스트 (일괄 변환 & 드래그 앤 드롭 구역)
        list_label = ttk.Label(main_frame, text="변환할 파일 목록 (Drag & Drop 지원):", style="Dark.TLabel")
        list_label.pack(anchor="w", pady=(0, 5))
        
        list_frame = ttk.Frame(main_frame, style="Dark.TFrame")
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.file_listbox = tk.Listbox(list_frame, bg="#2d2d2d", fg="white", selectbackground="#4CAF50", 
                                       borderwidth=0, highlightthickness=1, highlightcolor="#4CAF50", font=("맑은 고딕", 9))
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 드래그 앤 드롭 바인딩
        self.file_listbox.drop_target_register(DND_FILES)
        self.file_listbox.dnd_bind('<<Drop>>', self.handle_drop)

        btn_side_frame = ttk.Frame(list_frame, style="Dark.TFrame")
        btn_side_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        ttk.Button(btn_side_frame, text="추가", command=self.browse_audio).pack(fill=tk.X, pady=2)
        ttk.Button(btn_side_frame, text="제거", command=self.remove_selected).pack(fill=tk.X, pady=2)
        ttk.Button(btn_side_frame, text="비우기", command=self.clear_list).pack(fill=tk.X, pady=2)

        # 3. 옵션 설정 구역
        opt_frame = ttk.LabelFrame(main_frame, text="설정", padding="15", style="Dark.TLabelframe")
        opt_frame.pack(fill=tk.X, pady=20)

        # 배경 이미지 선택
        ttk.Label(opt_frame, text="배경 이미지:", style="Dark.TLabel").grid(row=0, column=0, sticky="w")
        self.img_entry = ttk.Entry(opt_frame, textvariable=self.image_path, width=45)
        self.img_entry.grid(row=0, column=1, padx=10)
        ttk.Button(opt_frame, text="찾기", command=self.browse_image).grid(row=0, column=2)

        # 파형 옵션 체크박스
        self.wave_check = tk.Checkbutton(opt_frame, text="오디오 파형(Waveform) 시각화 포함", 
                                         variable=self.use_waveform, bg="#2d2d2d", fg="white", 
                                         selectcolor="#1e1e1e", activebackground="#2d2d2d", 
                                         activeforeground="white", font=("맑은 고딕", 9))
        self.wave_check.grid(row=1, column=0, columnspan=3, sticky="w", pady=(10, 0))

        # 4. 진행도 및 버튼
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_val, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(10, 5))

        self.status_label = ttk.Label(main_frame, textvariable=self.status_msg, style="Status.TLabel")
        self.status_label.pack()

        self.convert_btn = ttk.Button(main_frame, text="일괄 변환 시작", style="Accent.TButton", command=self.start_batch_conversion)
        self.convert_btn.pack(fill=tk.X, ipady=8, pady=(15, 0))

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # 다크 테마 색상 정의
        bg_color = "#1e1e1e"
        frame_color = "#1e1e1e"
        text_color = "#ffffff"
        accent_color = "#4CAF50"

        style.configure("Dark.TFrame", background=frame_color)
        style.configure("Dark.TLabel", background=frame_color, foreground=text_color)
        style.configure("Dark.TLabelframe", background=frame_color, foreground=text_color)
        style.configure("Dark.TLabelframe.Label", background=frame_color, foreground=text_color)
        
        style.configure("Status.TLabel", background=frame_color, foreground="#aaaaaa", font=("맑은 고딕", 9))
        
        style.configure("TButton", font=("맑은 고딕", 9))
        style.configure("Accent.TButton", font=("맑은 고딕", 11, "bold"), background=accent_color, foreground="white")
        style.map("Accent.TButton", background=[('active', '#45a049')])

        style.configure("TProgressbar", thickness=10, background=accent_color)

    # --- 기능 함수들 ---
    def handle_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for f in files:
            if f.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg', '.flac')):
                if f not in self.audio_files:
                    self.audio_files.append(f)
                    self.file_listbox.insert(tk.END, os.path.basename(f))

    def browse_audio(self):
        files = filedialog.askopenfilenames(title="음성 파일 선택", filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.m4a *.flac")])
        for f in files:
            if f not in self.audio_files:
                self.audio_files.append(f)
                self.file_listbox.insert(tk.END, os.path.basename(f))

    def browse_image(self):
        f = filedialog.askopenfilename(title="이미지 선택", filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])
        if f: self.image_path.set(f)

    def remove_selected(self):
        idx = self.file_listbox.curselection()
        for i in reversed(idx):
            self.audio_files.pop(i)
            self.file_listbox.delete(i)

    def clear_list(self):
        self.audio_files.clear()
        self.file_listbox.delete(0, tk.END)

    def start_batch_conversion(self):
        if not self.audio_files:
            messagebox.showwarning("입력 누락", "변환할 파일을 추가해주세요.")
            return
        
        output_dir = filedialog.askdirectory(title="저장될 폴더를 선택하세요")
        if not output_dir: return

        self.convert_btn.config(state="disabled")
        thread = threading.Thread(target=self.batch_process, args=(output_dir,))
        thread.daemon = True
        thread.start()

    def batch_process(self, output_dir):
        total_files = len(self.audio_files)
        
        for i, audio in enumerate(self.audio_files):
            filename = os.path.splitext(os.path.basename(audio))[0] + ".mp4"
            output_path = os.path.join(output_dir, filename)
            
            self.root.after(0, lambda idx=i: self.status_msg.set(f"변환 중 ({idx+1}/{total_files}): {os.path.basename(audio)}"))
            self.run_ffmpeg(audio, self.image_path.get(), output_path)
            
            # 전체 진행률 업데이트
            overall_progress = ((i + 1) / total_files) * 100
            self.root.after(0, lambda v=overall_progress: self.progress_val.set(v))

        self.root.after(0, self.batch_finished)

    def run_ffmpeg(self, audio, image, output_path):
        # 파형 옵션에 따른 필터 구성
        if image and os.path.exists(image):
            input_v = ['-loop', '1', '-i', image]
            # 기본 이미지 필터 (852x480 맞춤)
            v_filter = "scale=852:480:force_original_aspect_ratio=decrease,pad=852:480:(ow-iw)/2:(oh-ih)/2,format=yuv420p"
        else:
            input_v = ['-f', 'lavfi', '-i', 'color=c=black:s=852x480:r=1']
            v_filter = "format=yuv420p"

        # 파형(Waveform) 필터 추가 로직
        if self.use_waveform.get():
            # [0:v]는 배경 이미지, [1:a]는 오디오
            # showwaves: 오디오를 시각화하여 하단에 오버레이
            v_filter += "[bg]; [1:a]showwaves=s=852x120:mode=line:colors=0x4CAF50[wave]; [bg][wave]overlay=0:H-h[v]"
            map_v = "[v]"
        else:
            map_v = "0:v"

        cmd = ['ffmpeg', '-y', '-hide_banner'] + input_v + ['-i', audio]
        cmd.extend([
            '-filter_complex', v_filter,
            '-map', map_v, '-map', '1:a',
            '-c:v', 'libx264', '-tune', 'stillimage', '-preset', 'faster', '-crf', '30', '-r', '1',
            '-c:a', 'aac', '-b:a', '128k', '-shortest', output_path
        ])

        si = None
        if os.name == 'nt':
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        subprocess.run(cmd, capture_output=True, startupinfo=si)

    def batch_finished(self):
        self.convert_btn.config(state="normal")
        self.status_msg.set("✅ 모든 변환이 완료되었습니다!")
        messagebox.showinfo("완료", "모든 파일의 일괄 변환이 끝났습니다.")

if __name__ == "__main__":
    # Tkinter 대신 TkinterDnD 사용 (드래그 앤 드롭 지원)
    root = TkinterDnD.Tk()
    app = DarkProConverter(root)
    root.mainloop()