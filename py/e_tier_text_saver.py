import os

class E_TierTextSaver:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "filename": ("STRING", {"forceInput": True}),
                "output_dir": ("STRING", {"default": "./ComfyUI/output"}),
                "text_to_remove": ("STRING", {"default": "<pad>"}),
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

    def save_cleaned_text(self, text, filename, output_dir, text_to_remove, unique_id=None, extra_pnginfo=None):
        try:
            
            if isinstance(text, list):
                text = "".join(text)
            if isinstance(filename, list):
                filename = filename[0]
            if isinstance(output_dir, list):
                output_dir = output_dir[0]
            if isinstance(text_to_remove, list):
                text_to_remove = text_to_remove[0]

            
            cleaned_text = text.replace(text_to_remove, "")
            base_name = os.path.splitext(os.path.basename(filename))[0]
            output_path = os.path.join(output_dir, base_name + ".txt")

            print(">>> E_TierTextSaver Start <<<")
            print(f"Save Path: {output_path}")
            print(">>> E_TierTextSaver End <<<")

            os.makedirs(output_dir, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned_text)

            
            if unique_id is not None and extra_pnginfo is not None:
                if isinstance(extra_pnginfo, list) and isinstance(extra_pnginfo[0], dict) and "workflow" in extra_pnginfo[0]:
                    workflow = extra_pnginfo[0]["workflow"]
                    node = next((x for x in workflow["nodes"] if str(x["id"]) == str(unique_id[0])), None)
                    if node:
                        node["widgets_values"] = [cleaned_text]

            return {
                "ui": {"text": [cleaned_text]},  
                "result": (cleaned_text,)        
            }

        except Exception as e:
            error_message = f"[E_TierTextSaver] Error occurred: {str(e)}"
            print(error_message)
            return {
                "ui": {"text": [error_message]},
                "result": (error_message,)
            }



NODE_CLASS_MAPPINGS = {
    "E_TierTextSaver": E_TierTextSaver,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "E_TierTextSaver": "Text Saver (E-Tier)",
}
