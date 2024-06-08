from krita import *

class ColorPaletteExtractor(Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("extractPalette", "Extract Palette from Active Layers", "tools/scripts")
        action.triggered.connect(self.extractPalette)

    def extractPalette(self):
        doc = Krita.instance().activeDocument()
        if not doc:
            QMessageBox.warning(None, "Error", "No active document found!")
            return

        colors = set()
        for layer in doc.topLevelNodes():
            if layer.visible():
                try:
                    pixel_data = layer.projectionPixelData(0, 0, layer.width(), layer.height()).data()
                    # Iterate through each pixel to extract colors
                    for i in range(0, len(pixel_data), 4):  # RGBA
                        r = pixel_data[i]
                        g = pixel_data[i+1]
                        b = pixel_data[i+2]
                        a = pixel_data[i+3]
                        if a > 0:  # Check if pixel is not transparent
                            colors.add((r, g, b))
                except Exception as e:
                    print(f"Error processing layer {layer.name()}: {str(e)}")

        # Create palette from collected colors
        palette = Palette()
        palette.setEntryCount(len(colors))
        for i, color in enumerate(colors):
            palette.setEntry(i, color[0], color[1], color[2], 255)  # RGB and full alpha

        # Save or use the palette as needed
        print("Palette extracted with colors:", colors)

def main():
    Krita.instance().addExtension(ColorPaletteExtractor(Krita.instance()))

if __name__ == "__main__":
    main()

