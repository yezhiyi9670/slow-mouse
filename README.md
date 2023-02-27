Slow Mouse
====

It is painful to carefully align your mouse when doing some sort of pixel-perfect dragging (for example when taking screenshots or drawing with mspaint), isn't it?

The aim of this project is simple - now you can slow your mouse down by simply holding a modifier key! In this way, you can easily align your mouse to a certain pixel.

> Note: This application is Windows only. It works by changing the mouse sensitivity settings, so won't work for a touchpad.

## Usage

To download prebuilt binaries, go to the Github releases page.

Launch the application and you will see a tray icon. Right click it to modify the settings.

It is meant to be minimalistic, so only the tray menu, no GUI in a window.

## Start on boot

This application does NOT start on boot automatically. You can configure it to do so by [dropping its shortcut into the Startup folder](https://cn.bing.com/search?q=dropping+shortcut+into+startup+folder).

## Testing and building

To test it, simply run `python slow-mouse.py`.

To build, run `build.cmd`. It relies on the `pyinstaller` package.
