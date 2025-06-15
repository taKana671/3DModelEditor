import sys
import math
from enum import Enum, auto
from datetime import datetime
from distutils.util import strtobool

import direct.gui.DirectGuiGlobals as DGG
from panda3d.core import Vec3, Vec2, Point3, LColor, Vec4
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import NodePath, TextNode
from panda3d.core import load_prc_file_data
from panda3d.core import OrthographicLens, Camera, MouseWatcher, PGTop
from panda3d.core import TransparencyAttrib, AntialiasAttrib
from direct.gui.DirectGui import DirectEntry, DirectFrame, DirectLabel, DirectButton, OkDialog
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock


from shapes import Cylinder
from shapes import Sphere
from shapes import Torus
from shapes import Cone
from shapes import Box
from shapes import RightTriangularPrism
from shapes import Plane
from shapes import EllipticalPrism
from shapes import Capsule
from shapes import CapsulePrism
from shapes import RoundedCornerBox
from shapes import RoundedEdgeBox
from validation import validate


# Without 'framebuffer-multisample' and 'multisamples' settings,
# there appears to be no effect of 'set_antialias(AntialiasAttrib.MAuto)'.
load_prc_file_data("", """
    win-size 1200 600
    window-title ProceduralShapes
    framebuffer-multisample 1
    multisamples 2
    """)


SHAPES = {
    'cone': Cone,
    'cylinder': Cylinder,
    'torus': Torus,
    'sphere': Sphere,
    'box': Box,
    'triangle': RightTriangularPrism,
    'plane': Plane,
    'capsule': Capsule,
    'capsule_prism': CapsulePrism,
    'elliptical_prism': EllipticalPrism,
    'rounded_corner_box': RoundedCornerBox,
    'rounded_edge_box': RoundedEdgeBox,
}


def is_int(str_val):
    try:
        int(str_val, 10)
    except ValueError:
        return False
    else:
        return True


def is_float(str_val):
    try:
        float(str_val)
    except ValueError:
        return False
    else:
        return True


def is_bool(str_val):
    try:
        strtobool(str_val)
    except ValueError:
        return False
    else:
        return True


class Status(Enum):

    SHOW_MODEL = auto()
    REPLACE_MODEL = auto()
    REPLACE_CLASS = auto()


class ModelDisplay(ShowBase):

    def __init__(self):
        super().__init__()
        self.disable_mouse()
        # self.setBackgroundColor(0.6, 0.6, 0.6)
        self.render.set_antialias(AntialiasAttrib.MAuto)
        self.setup_light()

        # Create model display region.
        self.camera_root = NodePath('camera_root')
        self.camera_root.reparent_to(self.render)
        self.mw3d_node = self.create_display_region(Vec4(0.3, 1.0, 0.0, 0.91))

        # Create gui regions.
        self.ctrl_aspect2d = self.create_gui_region(Vec4(0.0, 0.3, 0.0, 1.0), 'ctrl')
        self.slct_aspect2d = self.create_gui_region(Vec4(0.3, 1.0, 0.91, 1.0), 'slct')

        # Create gui.
        self.gui = Gui()
        self.gui.create_control_widgets(self.ctrl_aspect2d)
        self.gui.create_model_selector(self.slct_aspect2d)

        # Define variables.
        self.is_rotating = True
        # self.is_rotating = False
        self.show_wireframe = True
        self.dragging = False
        self.before_mouse_pos = None
        self.state = Status.SHOW_MODEL

        # Show default model.
        self.model_cls = Cone
        model_maker = self.model_cls()
        self.gui.set_default_values(model_maker)
        model = model_maker.create()
        self.dispay_model(model, hpr=Vec3(0, 0, 0))

        # self.accept('d', self.toggle_wireframe)
        # self.accept('r', self.toggle_rotation)

        self.accept('escape', sys.exit)
        self.accept('mouse1', self.mouse_click)
        self.accept('mouse1-up', self.mouse_release)
        self.taskMgr.add(self.update, 'update')

    def dispay_model(self, model, hpr=None, scale=4):
        # If hpr is None, inherit hpr from the current model and remove it.
        if hpr is None:
            hpr = self.model.get_hpr()
            self.model.remove_node()

        self.model = model
        self.model.set_pos_hpr_scale(Point3(0, 0, 0), hpr, scale)
        self.model.set_color(LColor(1, 0, 0, 1))
        self.model.reparent_to(self.render)

        # self.model = self.loader.load_model('torus_20241012130437.bam')
        # self.model.reparent_to(self.render)
        # self.model.set_texture(self.loader.load_texture('brick.jpg'))

        if self.show_wireframe:
            self.model.set_render_mode_wireframe()

    def output_bam_file(self):
        model_type = self.model_cls.__name__.lower()
        num = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'{model_type}_{num}.bam'

        output_model = self.model.copy_to(self.render)
        output_model.set_render_mode_filled()
        output_model.set_hpr(Vec3(0, 0, 0))
        output_model.set_color(LColor(1, 1, 1, 1))
        output_model.flatten_strong()

        # output_mode.clear_color()
        output_model.writeBamFile(filename)
        output_model.remove_node()

    def toggle_rotation(self):
        self.is_rotating = not self.is_rotating

    def toggle_wireframe(self):
        if self.show_wireframe:
            self.model.set_render_mode_filled()
        else:
            self.model.set_render_mode_wireframe()

        # self.toggle_wireframe()
        self.show_wireframe = not self.show_wireframe

    def calc_aspect_ratio(self, display_region):
        """Args:
            display_region (Vec4): (left, right, bottom, top)
            The range is from 0 to 1.
            0: the left and bottom; 1: the right and top.
        """
        props = self.win.get_properties()
        window_size = props.get_size()

        region_w = display_region.y - display_region.x
        region_h = display_region.w - display_region.z
        display_w = int(window_size.x * region_w)
        display_h = int(window_size.y * region_h)

        gcd = math.gcd(display_w, display_h)
        w = display_w / gcd
        h = display_h / gcd
        aspect_ratio = w / h

        return aspect_ratio

    def calc_scale(self, region_size):
        aspect_ratio = self.get_aspect_ratio()

        w = region_size.y - region_size.x
        h = region_size.w - region_size.z
        new_aspect_ratio = aspect_ratio * w / h

        if aspect_ratio > 1.0:
            s = 1. / h
            return Vec3(s / new_aspect_ratio, 1.0, s)
        else:
            s = 1.0 / w
            return Vec3(s, 1.0, s * new_aspect_ratio)

    def create_mouse_watcher(self, name, display_region):
        mw_node = MouseWatcher(name)
        # Gets MouseAndKeyboard, the parent of base.mouseWatcherNode
        # that passes mouse data into MouseWatchers,
        input_ctrl = self.mouseWatcher.get_parent()
        input_ctrl.attach_new_node(mw_node)
        # Restricts new MouseWatcher to the intended display region.
        mw_node.set_display_region(display_region)

        return mw_node

    def create_display_region(self, region_size):
        """Create the region to display a model.
            Args:
                size (Vec4): Vec4(left, right, bottom, top)
        """
        region = self.win.make_display_region(region_size)

        # create custom camera.
        cam = NodePath(Camera('cam3d'))
        aspect_ratio = self.calc_aspect_ratio(region_size)
        cam.node().get_lens().set_aspect_ratio(aspect_ratio)
        region.set_camera(cam)
        self.camNode.set_active(False)

        cam.set_pos(Point3(30, -30, 0))
        cam.look_at(Point3(0, 0, 0))
        cam.reparent_to(self.camera_root)

        # create a MouseWatcher of the region.
        mw3d_node = self.create_mouse_watcher('mw3d', region)

        return mw3d_node

    def create_gui_region(self, region_size, name):
        """Create the custom 2D region for gui.
            Args:
                size (Vec4): Vec4(left, right, bottom, top)
        """
        region = self.win.make_display_region(region_size)
        region.set_sort(20)
        # region.set_clear_color((0.5, 0.5, 0.5, 1.))
        # region.set_clear_color_active(True)

        # create custom camera.
        cam = NodePath(Camera(f'cam_{name}'))
        lens = OrthographicLens()
        lens.set_film_size(2, 2)
        lens.set_near_far(-1000, 1000)
        cam.node().set_lens(lens)

        gui_render2d = NodePath(f'render2d_{name}')
        gui_render2d.set_depth_test(False)
        gui_render2d.set_depth_write(False)

        cam.reparent_to(gui_render2d)
        region.set_camera(cam)

        gui_aspect2d = gui_render2d.attach_new_node(PGTop(f'gui_{name}'))
        scale = self.calc_scale(region_size)
        gui_aspect2d.set_scale(scale)

        # create a MouseWatcher of the region.
        mw2d_nd = self.create_mouse_watcher(f'mw_{name}', region)
        gui_aspect2d.node().set_mouse_watcher(mw2d_nd)

        return gui_aspect2d

    def setup_light(self):
        ambient_light = NodePath(AmbientLight('ambient_light'))
        ambient_light.reparent_to(self.render)
        ambient_light.node().set_color(LColor(0.6, 0.6, 0.6, 1.0))
        self.render.set_light(ambient_light)

        directional_light = NodePath(DirectionalLight('directional_light'))
        directional_light.node().get_lens().set_film_size(200, 200)
        directional_light.node().get_lens().set_near_far(1, 100)
        directional_light.node().set_color(LColor(1, 1, 1, 1))
        directional_light.set_pos_hpr(Point3(0, 0, 50), Vec3(-30, -45, 0))
        # directional_light.node().show_frustom()
        self.render.set_light(directional_light)
        directional_light.node().set_shadow_caster(True)
        self.render.set_shader_auto()

    def mouse_click(self):
        self.dragging = True
        self.dragging_start_time = globalClock.get_frame_time()

    def mouse_release(self):
        self.dragging = False
        self.before_mouse_pos = None

    def rotate_camera(self, mouse_pos, dt):
        if self.before_mouse_pos:
            angle = Vec3()

            if (delta := mouse_pos.x - self.before_mouse_pos.x) < 0:
                angle.x += 180
            elif delta > 0:
                angle.x -= 180

            if (delta := mouse_pos.y - self.before_mouse_pos.y) < 0:
                angle.z -= 180
            elif delta > 0:
                angle.z += 180

            angle *= dt
            self.camera_root.set_hpr(self.camera_root.get_hpr() + angle)

        self.before_mouse_pos = Vec2(mouse_pos.xy)

    def rotate_model(self, dt):
        angle = self.model.get_hpr() + 20 * dt

        if angle > 360:
            angle = 0

        self.model.set_hpr(angle)

    def get_input_value(self, label_txt, str_val):
        if is_int(str_val):
            return int(str_val)

        if is_float(str_val):
            return float(str_val)

        if is_bool(str_val):
            return bool(strtobool(str_val))

        raise ValueError(f'{label_txt}: input value is invalid.')

    def change_model_types(self, name):
        self.model_cls = SHAPES[name]
        self.state = Status.REPLACE_CLASS

    def reflect_changes(self):
        self.state = Status.REPLACE_MODEL

    def create_new_model(self):
        params = {}

        try:
            for label, entry in self.gui.entries.items():
                if not (label_txt := label['text']):
                    break

                input_value = self.get_input_value(label_txt, entry.get())
                validate(label_txt, input_value)
                params[label_txt] = input_value

            new_model = self.model_cls(**params).create()

        except ValueError as e:
            # An error may occur in the self.get_input_value metho
            # or the create methods of shape classes.
            error_msg = e.args[0]
            k, msg = error_msg.split(': ')
            name = REPLACE_NAMES[k] if k in REPLACE_NAMES else k
            self.gui.show_dialog(f'{name}: {msg}')
        else:
            return new_model

    def update(self, task):
        dt = globalClock.get_dt()

        match self.state:

            case Status.SHOW_MODEL:
                if self.is_rotating:
                    self.rotate_model(dt)

                if self.mw3d_node.has_mouse():
                    mouse_pos = self.mw3d_node.get_mouse()

                    if self.dragging:
                        if globalClock.get_frame_time() - self.dragging_start_time >= 0.2:
                            self.rotate_camera(mouse_pos, dt)

            case Status.REPLACE_MODEL:
                if new_model := self.create_new_model():
                    self.dispay_model(new_model)
                self.state = Status.SHOW_MODEL

            case Status.REPLACE_CLASS:
                model_maker = self.model_cls()
                self.gui.set_default_values(model_maker)
                self.dispay_model(model_maker.create())
                self.state = Status.SHOW_MODEL

        return task.cont


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

    def __init__(self):
        self.font = base.loader.load_font('fonts/DejaVuSans.ttf')
        self.text_size = 0.05

        base.accept('tab', self.change_focus, [True])
        base.accept('shift-tab', self.change_focus, [False])

    def create_control_widgets(self, parent):
        frame = Frame(
            parent,
            Vec4(-0.6, 0.6, -1., 1.),  # (left, right, bottom, top)
        )

        last_z = self.create_input_boxes(frame)
        _ = self.create_control_btns(frame, last_z)

    def create_model_selector(self, parent):
        frame = Frame(
            parent,
            Vec4(-1.4, 1.4, -0.09, 0.09),  # (left, right, bottom, top)
        )

        self.create_model_select_btns(frame)

    def create_model_select_btns(self, parent):
        start_x = -1.31
        start_z = 0
        btn_size = 0.16
        half = btn_size / 2

        for i, text in enumerate(SHAPES.keys()):
            x = start_x + i * btn_size

            DirectButton(
                parent=parent,
                image=f'icons/{text}.png',
                image_scale=0.05,
                pos=Point3(x, 0, start_z),
                relief=DGG.RAISED,
                frameSize=(-half, half, -half, half),
                frameColor=self.frame_color,
                text_fg=self.text_color,
                text_scale=self.text_size,
                text_font=self.font,
                text_pos=(0, -0.01),
                borderWidth=(0.01, 0.01),
                command=base.change_model_types,
                extraArgs=[text]
            )

    def create_input_boxes(self, parent):
        self.entries = {}
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

            DirectButton(
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
        return z

    def set_default_values(self, instance):
        keys = [k for k in instance.__dict__.keys() if k not in EX_COMMON]

        if (name := instance.__class__.__name__) in EX_INDIVI:
            keys = [k for k in keys if k not in EX_INDIVI[name]]

        key_cnt = len(keys)

        for i, (label, entry) in enumerate(self.entries.items()):
            if i < key_cnt:
                k = keys[i]
                label_txt = REPLACE_NAMES[k] if k in REPLACE_NAMES else k
                label.setText(label_txt)
                defalut_val = instance.__dict__[k]
                entry.enterText(str(defalut_val))
                continue

            label.setText('')
            entry.enterText('')

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

    def show_dialog(self, msg):
        self.dialog = OkDialog(
            dialogName='validation',
            frameSize=(-1, 1, -0.2, 0.1),
            frameColor=self.frame_color,
            relief=DGG.FLAT,
            pos=Point3(0.5, 0, 0.8),
            midPad=0.02,
            text=msg,
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

    def withdraw_dialog(self, btn):
        def withdraw(task):
            self.dialog.cleanup()
            return task.done
        base.taskMgr.do_method_later(0.5, withdraw, 'withdraw')


EX_COMMON = ('bottom_center', 'top_center', 'center', 'fmt', 'color', 'stride')

EX_INDIVI = {
    'CapsulePrism': ['open_left', 'open_right', 'open_front', 'open_back'],
    'RoundedCornerBox': ['open_left', 'open_right', 'open_front', 'open_back'],
    'Capsule': ['start_slice_cap', 'end_slice_cap', 'segs_tc', 'segs_bc'],
    'RoundedEdgeBox': ['open_left', 'open_right', 'open_front', 'open_back'],
}


REPLACE_NAMES = {
    'segs_sc_r': 'slice_caps_radial',
    'segs_sc_a': 'slice_caps_axial',
    'segs_bc': 'segs_bottom_cap',
    'segs_tc': 'segs_top_cap',
    'segs_sc': 'segs_slice_caps',
    'segs_sssc': 'section_slice_start_cap',
    'segs_ssec': 'section_slice_end_cap',
    'segs_rssp': 'ring_slice_start_cap',
    'segs_rsec': 'ring_slice_end_cap',
    'c_radius': 'corner_radius',
    'rf_left': 'rounded_f_left',
    'rf_right': 'rounded_f_right',
    'rb_left': 'rounded_b_left',
    'rb_right': 'rounded_b_right'
}


if __name__ == '__main__':
    app = ModelDisplay()
    app.run()