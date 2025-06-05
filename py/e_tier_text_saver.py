import os
import yaml
import html
from types import MappingProxyType

WL_CONFIG_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), "config", "E_Tier_WL.yaml"))

def load_whitelist():
    try:
        print(f"[E_TierTextSaver] Loading whitelist from: {WL_CONFIG_PATH}")
        with open(WL_CONFIG_PATH, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not isinstance(data, dict) or "whitelist" not in data:
                raise ValueError("Invalid whitelist YAML format")
            whitelist = {}
            for label, path in data["whitelist"].items():
                real_path = os.path.realpath(path)
                whitelist[label] = real_path
            return MappingProxyType(whitelist)
    except Exception as e:
        print(f"[E_TierTextSaver] Failed to load whitelist file: {e}")
        return MappingProxyType({})

WHITELIST_LABELS = load_whitelist()

class E_TierTextSaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "filename": ("STRING", {"forceInput": True}),
                "text_to_remove": ("STRING", {"default": "<pad>"}),
                "save_to": (list(WHITELIST_LABELS.keys()), {"default": list(WHITELIST_LABELS.keys())[0] if WHITELIST_LABELS else None})
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO"
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "save_cleaned_text"
    CATEGORY = "E_Tier/Text"
    OUTPUT_NODE = True

    def __init__(self):
        self.last_error_message = None

    def validate_directory_path(self, label):
        if label not in WHITELIST_LABELS:
            raise ValueError(f"Unknown output directory label: {label}")
        resolved_path = WHITELIST_LABELS[label]
        if os.path.islink(resolved_path):
            raise ValueError("Symbolic link not allowed")
        if not os.path.isdir(resolved_path):
            raise ValueError(f"Path does not exist or is not a directory: {resolved_path}")
        if not resolved_path.startswith(WHITELIST_LABELS[label]):
            raise ValueError("Symbolic link attack detected")
        return resolved_path

    def sanitize_input(self, text):
        original = text
        blocked_patterns = [
            "<script>", "</script>", "eval(", "exec(", "compile(", "os.system(",
            "os.popen(", "subprocess.call(", "subprocess.Popen(", "__import__",
            "__builtins__", "open(", "input(", "getattr(", "setattr(",
            "globals(", "locals(", "sys.modules", "shlex.split(",
            "marshal.loads(", "pickle.loads(", "base64.b64decode(",
            "ctypes.", "ffi.", "socket.", "urllib.request.urlopen(",
            "requests.get("
        ]
        for pattern in blocked_patterns:
            if pattern in text:
                text = text.replace(pattern, "")
        if text != original:
            print("[E_TierTextSaver] Text was sanitized for safety.")
        return text

    def sanitize_filename(self, name):
        original = name
        forbidden_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        sanitized = "".join(c if c not in forbidden_chars else "_" for c in name).strip()
        if len(sanitized) > 100:
            sanitized = sanitized[:100]
            print("[E_TierTextSaver] Filename too long. Truncating to 100 characters.")
        if sanitized == "":
            print("[E_TierTextSaver] Filename was empty. Using default name: 'untitled'")
            return "untitled"
        if sanitized != original:
            print("[E_TierTextSaver] Filename was sanitized for safety.")
        return sanitized

    def save_cleaned_text(self, text, filename, text_to_remove, save_to, unique_id=None, extra_pnginfo=None):
        try:
            if isinstance(text, list):
                text = "".join(text)
            if isinstance(filename, list):
                filename = filename[0]
            if isinstance(text_to_remove, list):
                text_to_remove = text_to_remove[0]
            if isinstance(save_to, list):
                save_to = save_to[0]

            cleaned_text = text.replace(text_to_remove, "")
            if cleaned_text != text:
                print(f"[E_TierTextSaver] Removed unwanted token: '{text_to_remove}'")
            cleaned_text = self.sanitize_input(cleaned_text)
            cleaned_text.encode("utf-8")

            base_name = os.path.splitext(os.path.basename(filename))[0]
            safe_base_name = self.sanitize_filename(base_name)
            output_dir = self.validate_directory_path(save_to)
            output_path = os.path.join(output_dir, safe_base_name + ".txt")

            if len(output_path) >= 255:
                error_message = "[E_TierTextSaver] Error: Path too long (limit: 255 characters)"
                if self.last_error_message != error_message:
                    self.last_error_message = error_message
                    print(error_message)
                return {
                    "ui": {"text": [error_message]},
                    "result": (error_message,)
                }

            if os.path.exists(output_path):
                print("[E_TierTextSaver] Overwriting existing file")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)

            print(f"[E_TierTextSaver] Text File Created Successfully at:\n{output_path}")

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

NODE_CLASS_MAPPINGS = {
    "E_TierTextSaver": E_TierTextSaver
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "E_TierTextSaver": "Text Saver (E-Tier)"
}
