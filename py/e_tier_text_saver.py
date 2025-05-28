import os
import html

class E_TierTextSaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "filename": ("STRING", {"forceInput": True}),
                "text_to_remove": ("STRING", {"default": "<pad>"}),
                "output_dir": ("STRING", {"default": "./ComfyUI/output", "forceInput": False}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "save_cleaned_text"
    CATEGORY = "E_Tier/Text"
    OUTPUT_NODE = True

    def __init__(self):
        self.last_output = None
        self.last_error_message = None

    def validate_directory_path(self, path):
        abs_path = os.path.abspath(path)

        # 차단된 시스템 경로
        forbidden_paths = [
            "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)", "C:\\Users\\Default"
        ]
        for fp in forbidden_paths:
            if abs_path.lower().startswith(fp.lower()):
                raise ValueError(f"Access to system directory is forbidden: {abs_path}")

        # 경로 탈출 및 위험 문자 차단
        if ".." in path or path.strip().startswith(("/", "\\")):
            raise ValueError(f"Suspicious relative path: {path}")
        dangerous_chars = ['|', ';', '&', '$', '<', '>', '"']
        if any(c in path for c in dangerous_chars):
            raise ValueError(f"Illegal character detected in path: {path}")

        # 존재 여부와 유형 확인
        if os.path.exists(abs_path):
            if not os.path.isdir(abs_path):
                raise ValueError(f"Path exists but is not a directory: {abs_path}")
        else:
            if os.path.splitext(abs_path)[1]:  # 확장자 존재 (예: .txt, .py 등)
                raise ValueError(f"File path detected but does not exist: {abs_path}")
            else:
                raise ValueError(f"Directory does not exist: {abs_path}")

        return abs_path

    def save_cleaned_text(self, text, filename, text_to_remove, output_dir, unique_id=None, extra_pnginfo=None):
        try:
            if isinstance(text, list):
                text = "".join(text)
            if isinstance(filename, list):
                filename = filename[0]
            if isinstance(text_to_remove, list):
                text_to_remove = text_to_remove[0]
            if isinstance(output_dir, list):
                output_dir = output_dir[0]

            # 텍스트 정제 및 필터링
            cleaned_text = text.replace(text_to_remove, "")
            cleaned_text = self.sanitize_input(cleaned_text)

            base_name = os.path.splitext(os.path.basename(filename))[0]
            output_dir = self.validate_directory_path(output_dir)
            output_path = os.path.join(output_dir, base_name + ".txt")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)

            if self.last_output != cleaned_text:
                self.last_output = cleaned_text
                print(f"[E_TierTextSaver] Security Check Passed: Text Sanitized Successfully.")
                print(f"[E_TierTextSaver] Text File Created Successfully at {output_path}")

            return {
                "ui": {"text": [cleaned_text], "output_dir": output_path},
                "result": (cleaned_text,)
            }

        except Exception as e:
            error_message = f"[E_TierTextSaver] Error occurred: {str(e)}"
            if self.last_error_message != error_message:
                self.last_error_message = error_message
                print(f"[E_TierTextSaver] Error: {error_message}")
            return {
                "ui": {"text": [self.last_error_message]},
                "result": (self.last_error_message,)
            }

    def sanitize_input(self, text):
        """
        보안 상 문제되는 문자열 제거
        """
        text = html.escape(text)
        blocked_patterns = ["<script>", "</script>", "eval(", "os.system(", "import", "exec("]
        for pattern in blocked_patterns:
            if pattern in text:
                print(f"[E_TierTextSaver] Security Warning: Blocked harmful code pattern: {pattern}")
            text = text.replace(pattern, "")
        return text


NODE_CLASS_MAPPINGS = {
    "E_TierTextSaver": E_TierTextSaver,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "E_TierTextSaver": "Text Saver (E-Tier)",
}
