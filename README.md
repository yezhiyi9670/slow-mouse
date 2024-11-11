Slow Mouse
====

> [Buy me a coffee](https://afdian.net/a/yezhiyi9670) if you like this project.

Just as the name suggests, the aim of this project is simple - now you can slow your mouse down by simply holding a modifier key. In this way, you can easily align your mouse to a certain pixel. **It also works for touchpads on Windows 11 24H2 or later**.

It's useful under circumstances such as:

- Dragging some slider such as the volume slider, and trying to obtain an accurate value.
- Trying to resize a window or a box but simply having trouble aligning the mouse to the anchor.
- Trying to select an accurate rectangle of the screen for screenshot or capturing.
- Trying to drag a piece of image to an accurate place. (it's tencent's captcha, isn't it?)

> Note: This application is Windows only. It works by changing various settings ([details in code here](./app/winparam_values.py)), and will not affect games that are using raw mouse input (e.g. Minecraft 1.14+ under default settings).

## Usage

If you just want to use it, download `exe` in [**GitHub Releases**](https://github.com/yezhiyi9670/slow-mouse/releases).

Launch the application and you will see a tray icon. Right click it to modify the settings. Note that as of version 1.0.0, **the app does nothing by default**. You have to enable the slow-down functionalities in the settings.

## Start on boot

This application does NOT start on boot automatically. You can configure it to do so by [dropping its shortcut into the Startup folder](https://cn.bing.com/search?q=Add+shortcut+to+startup).

## Testing and building

To test it, simply run `python slow-mouse.py`.

To build, run `build.cmd`. It relies on the `pyinstaller` package.

Check `requirements.txt` if necessary.
