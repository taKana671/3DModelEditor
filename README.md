# 3DModelEditor

Provides an editor for procedurally creating 3D shape models using source code from the [shapes](https://github.com/taKana671/shapes) repository, while visually seeing how the shape changes when parameters are changed.

![Image](https://github.com/user-attachments/assets/f0ca5f64-3fab-4d1e-8802-c4eb55fae32e)


# Requirements
* Panda3D 1.10.15
* numpy 2.2.4

# Environment
* Python 3.12
* Windows11

# Usage of editor

### Clone this repository with submodule.

```
git clone --recursive https://github.com/taKana671/3DModelEditor.git
```

### Start the editor

```
>>> cd 3DModelEditor
>>> python model_editor.py
```

* 3D shape icon buttons change 3D shape models.
* Change the parameters in the left input boxes and click the [Reflect Changes] button to reflect the changes in the 3D model.
* [Toggle Wireframe] button toggles between with and without wireframe.
* [Toggle Rotation] toggles between rotating and stopping the 3D model.
