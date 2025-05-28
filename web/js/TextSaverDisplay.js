import { app } from "../../../scripts/app.js";
import { ComfyWidgets } from "../../../scripts/widgets.js";

app.registerExtension({
	name: "E_Tier.TextSaverDisplay",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "E_TierTextSaver") {
			function populate(text) {
				const values = Array.isArray(text) ? text : [text];

				
				this.widgets = this.widgets.filter(w => {
					if (w.name?.startsWith?.("text_output_")) {
						w.onRemove?.();
						return false;
					}
					return true;
				});

				for (let i = 0; i < values.length; i++) {
					const w = ComfyWidgets["STRING"](
						this,
						"text_output_" + i,
						["STRING", { multiline: true }],
						app
					).widget;
					w.inputEl.readOnly = true;
					w.inputEl.style.opacity = 0.6;
					w.value = values[i];
				}

				requestAnimationFrame(() => {
					const sz = this.computeSize();
					this.onResize?.(sz);
					app.graph.setDirtyCanvas(true, false);
				});
			}

			const onExecuted = nodeType.prototype.onExecuted;
			nodeType.prototype.onExecuted = function (message) {
				onExecuted?.apply(this, arguments);
				if (message.text) populate.call(this, message.text);
			};

			const VALUES = Symbol();
			const configure = nodeType.prototype.configure;
			nodeType.prototype.configure = function () {
				this[VALUES] = arguments[0]?.widgets_values;
				return configure?.apply(this, arguments);
			};

			const onConfigure = nodeType.prototype.onConfigure;
			nodeType.prototype.onConfigure = function () {
				onConfigure?.apply(this, arguments);
				const widgets_values = this[VALUES];
				if (widgets_values?.length > 4) {
					requestAnimationFrame(() => {
						populate.call(this, widgets_values.slice(4));
					});
				}
			};
		}
	},
});
