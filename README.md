Slow Mouse
====

> [Buy me a coffee](https://afdian.net/a/yezhiyi9670) if you like this project.

Just as the name suggests, the aim of this project is simple - now you can slow your mouse down by simply holding a modifier key. In this way, you can easily align your mouse to a certain pixel. It's useful under circumstances such as:

- Dragging some slider such as the volume slider, and trying to obtain an accurate value.
- Trying to resize a window or a box but simply having trouble aligning the mouse to the anchor.
- Trying to select an accurate rectangle of the screen for screenshot or capturing.
- Trying to drag a piece of image to an accurate place. (it's tencent's captcha, isn't it?)

> Note: This application is Windows only. It works by changing the mouse sensitivity settings, so won't work for a touchpad. It should also not affect games that are using raw mouse input.

## Usage

To download prebuilt binaries, go to the Github releases page.

Launch the application and you will see a tray icon. Right click it to modify the settings.

## Start on boot

This application does NOT start on boot automatically. You can configure it to do so by [dropping its shortcut into the Startup folder](https://cn.bing.com/search?q=dropping+shortcut+into+startup+folder).

## Testing and building

To test it, simply run `python slow-mouse.py`.

To build, run `build.cmd`. It relies on the `pyinstaller` package.
