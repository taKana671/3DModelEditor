from direct.gui.DirectGui import DirectEntry, DirectFrame, DirectLabel, DirectButton, OkDialog
import direct.gui.DirectGuiGlobals as DGG
from panda3d.core import TransparencyAttrib
from panda3d.core import Point3, LColor, Vec4
from panda3d.core import TextNode


class Frame(DirectFrame):

    def __init__(self, parent, size):
        super().__init__(
            parent=parent,
            frameSize=size,
            frameColor=Gui.frame_color,
            pos=Point3(0, 0, 0),
            relief=DGG.SUNKEN,
            borderWidth=(0.01, 0.01)
        )
        self.initialiseoptions(type(self))
        self.set_transparency(TransparencyAttrib.MAlpha)


class Gui:

    frame_color = LColor(0.6, 0.6, 0.6, 1)
    text_color = LColor(1.0, 1.0, 1.0, 1.0)
    text_size = 0.05
    font_file = 'fonts/DejaVuSans.ttf'

    def __init__(self, controller_parent, selector_parent, model_names):
        self.font = base.loader.load_font(self.font_file)
        self.entries = {}
        self.buttons = []
        self.create_widgets(controller_parent, selector_parent, model_names)

        base.accept('tab', self.change_focus, [True])
        base.accept('shift-tab', self.change_focus, [False])

    def create_widgets(self, controller_parent, selector_parent, model_names):
        self.create_controller_area(controller_parent)
        self.create_selector_area(selector_parent, model_names)

    def create_controller_area(self, parent):
        frame = Frame(
            parent,
            Vec4(-0.6, 0.6, -1., 1.),  # (left, right, bottom, top)
        )

        last_z = self.create_input_boxes(frame)
        _ = self.create_control_btns(frame, last_z)

    def create_selector_area(self, parent, model_names):
        frame = Frame(
            parent,
            Vec4(-1.4, 1.4, -0.09, 0.09),  # (left, right, bottom, top)
        )

        self.create_model_select_btns(frame, model_names)

    def create_model_select_btns(self, parent, model_names):
        """Create a button that calls change_model_types when clicked.
           The parameter passed to change_model_types is the model name.
            Args:
                parent (Frame): a parent of the buttons.
                model_names (list): a list of the model names(string).
        """
        start_x = -1.31
        start_z = 0
        btn_size = 0.16
        half = btn_size / 2

        for i, model_name in enumerate(model_names):
            x = start_x + i * btn_size

            btn = DirectButton(
                parent=parent,
                pos=Point3(x, 0, start_z),
                relief=DGG.RAISED,
                frameSize=(-half, half, -half, half),
                frameColor=self.frame_color,
                borderWidth=(0.01, 0.01),
                text_pos=(0, -0.01),
                image=f'icons/{model_name}.png',
                image_scale=0.05,
                command=base.change_model_types,
                extraArgs=[model_name]
            )
            self.buttons.append(btn)

    def create_input_boxes(self, parent):
        start_z = 0.88

        for i in range(16):
            z = start_z - i * 0.1

            label = DirectLabel(
                parent=parent,
                pos=Point3(0.2, 0.0, z),
                frameColor=LColor(1, 1, 1, 0),
                text='',
                text_fg=self.text_color,
                text_font=self.font,
                text_scale=self.text_size,
                text_align=TextNode.ARight
            )

            entry = DirectEntry(
                parent=parent,
                pos=Point3(0.25, 0, z),
                relief=DGG.SUNKEN,
                frameColor=self.frame_color,
                text_fg=self.text_color,
                width=5,
                scale=self.text_size,
                numLines=1,
                text_font=self.font,
                initialText='',
            )
            self.entries[label] = entry

            if i == 0:
                entry['focus'] = 1

        return z

    def create_control_btns(self, parent, start_z):
        buttons = [
            ('Reflect Changes', base.reflect_changes),
            ('Output BamFile', base.output_bam_file),
            ('Toggle Wireframe', base.toggle_wireframe),
            ('Toggle Rotation', base.toggle_rotation),
        ]
        start_z -= 0.18

        for i, (text, cmd) in enumerate(buttons):
            q, mod = divmod(i, 2)
            x = -0.255 + mod * 0.51
            z = start_z - 0.1 * q

            btn = DirectButton(
                parent=parent,
                pos=Point3(x, 0, z),
                relief=DGG.RAISED,
                frameSize=(-0.255, 0.255, -0.05, 0.05),
                frameColor=self.frame_color,
                borderWidth=(0.01, 0.01),
                text=text,
                text_fg=self.text_color,
                text_scale=self.text_size,
                text_font=self.font,
                text_pos=(0, -0.01),
                command=cmd
            )
            self.buttons.append(btn)

        return z

    def set_default_values(self, params):
        """Set default values for entry boxes.
            Args:
                params (dict): {parameter name: its value,,,,}
        """
        keys = [*params.keys()]
        key_cnt = len(keys)

        for i, (label, entry) in enumerate(self.entries.items()):
            if i < key_cnt:
                k = keys[i]
                label.setText(k)
                entry.enterText(str(params[k]))
                continue

            label.setText('')
            entry.enterText('')

    def get_input_values(self):
        """Returns the values entered in the entry box.
        """
        return {param_name: entry.get() for label, entry in self.entries.items()
                if (param_name := label['text'])}

    def change_focus(self, go_down):
        entries = list(self.entries.values())

        for i, entry in enumerate(entries):
            if entry['focus']:
                if go_down:
                    next_idx = i + 1 if i < len(self.entries) - 1 else 0
                else:
                    next_idx = len(self.entries) - 1 if i == 0 else i - 1

                entry['focus'] = 0
                entries[next_idx]['focus'] = 1
                break

    def show_dialog(self, msgs):
        self.change_buttons_state(DGG.DISABLED)

        lines = len(msgs)
        bottom = -0.001 * lines / 2 - 0.15
        top = 0.001 * lines / 2 + 0.01

        self.dialog = OkDialog(
            dialogName='validation',
            frameSize=(-1.2, 1.2, bottom, top),
            # frameSize=(-1, 1, -0.2, 0.1),
            frameColor=(1, 1, 1, 0),
            # frameColor=self.frame_color,
            relief=DGG.FLAT,
            pos=Point3(0.5, 0, 0.0),
            midPad=0.02,
            text=msgs,
            text_scale=self.text_size,
            text_font=self.font,
            text_fg=self.text_color,
            buttonSize=(-0.08, 0.08, -0.05, 0.05),
            buttonTextList=['OK'],
            button_frameColor=self.frame_color,
            button_text_pos=(0, -0.01),
            button_text_scale=0.04,
            button_text_fg=self.text_color,
            command=self.withdraw_dialog
        )

    def change_buttons_state(self, state):
        for button in self.buttons:
            button['state'] = state

    def withdraw_dialog(self, btn):
        def withdraw(task):
            self.dialog.cleanup()
            self.change_buttons_state(DGG.NORMAL)
            return task.done

        base.taskMgr.do_method_later(0.2, withdraw, 'withdraw')
