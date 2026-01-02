# 3DModelEditor

Provides an editor for procedurally creating 3D shape models using source code from the [shapes](https://github.com/taKana671/shapes) repository, while visually seeing how the shape changes when parameters are changed. The values of the entered parameters are validated. If the conditions are not met, an error message is displayed on the screen.

![Image](https://github.com/user-attachments/assets/f0ca5f64-3fab-4d1e-8802-c4eb55fae32e)

# 3D models that can currently be created

![Image](https://github.com/user-attachments/assets/80f25c17-43d3-4722-a0b2-fc3e1b386bbd)
![Image](https://github.com/user-attachments/assets/53c42085-b5e5-445c-919e-cb305e61686f)
![Image](https://github.com/user-attachments/assets/28bcdd21-c640-442f-ad01-05a8e0fa1f07)

# Requirements
* Panda3D 1.10.16
* numpy 2.2.6
* pydantic 2.12.5

# Environment
* Python 3.13
* Windows11
* Ubuntu 24.04.3 

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
* Change the parameters in the left input boxes and click the [Reflect Changes] button to reflect the changes in the 3D model.The entered parameter values are validated, and if the conditions are not met, error messages will appear on the screen. Correct the values and click the [OK] button.
* [Toggle Wireframe] button toggles between with and without wireframe.
* [Toggle Rotation] toggles between rotating and stopping the 3D model.



