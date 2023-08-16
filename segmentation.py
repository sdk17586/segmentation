import tkinter as tk
from PIL import Image, ImageTk
import json
import os

class SegmentationLabelingTool:
    def __init__(self, root, image_paths):
        self.root = root
        self.canvas = tk.Canvas(root, width=500, height=500, bg='white')
        self.canvas.pack()
        
        self.image_paths = image_paths
        self.current_image_index = 0
        self.load_current_image()
        
        self.coordinates = []
        self.current_class = "default_class"
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.clear_button = tk.Button(root, text="Clear", command=self.clear_coordinates)
        self.clear_button.pack()
        self.save_button = tk.Button(root, text="Save", command=self.save_coordinates)
        self.save_button.pack()
        self.next_button = tk.Button(root, text="Next Image (Right Arrow)", command=self.next_image)
        self.next_button.pack()
        self.prev_button = tk.Button(root, text="Previous Image (Left Arrow)", command=self.prev_image)
        self.prev_button.pack()
        
        self.class_entry = tk.Entry(root, width=20)
        self.class_entry.pack()
        
        root.bind("<Right>", self.next_image)  # 오른쪽 화살표
        root.bind("<Left>", self.prev_image)    # 왼쪽 화살표
    
    def load_current_image(self):
        self.clear_coordinates()  # 이전 이미지의 라벨링 지우기
        image_path = self.image_paths[self.current_image_index]
        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        
    def on_click(self, event):
        x, y = event.x, event.y
        self.coordinates.append({"x": x, "y": y})
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill='red')
    
    def clear_coordinates(self):
        self.coordinates = []
        self.canvas.delete("all")
    
    def save_coordinates(self):
        save_path = os.path.splitext(self.image_paths[self.current_image_index])[0] + ".dat"
        class_id = hash(self.current_class) % 100000
        class_data = {
            "classId": str(class_id),
            "className": self.current_class,
            "color": "#e27c80",
            "cursor": "isPolygon",
            "needCount": -1,
            "position": self.coordinates,
            "showTf": True
        }
        data = {"polygonData": [class_data], "brushData": [], "totalClass": [self.current_class]}
        with open(save_path, 'w') as json_file:
            json.dump(data, json_file)
        print("Coordinates saved to", save_path)
    
    def next_image(self, event=None):
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.load_current_image()
            self.current_class = self.class_entry.get() or "default_class"
    
    def prev_image(self, event=None):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_current_image()
            self.current_class = self.class_entry.get() or "default_class"

def main():
    root = tk.Tk()
    root.title("Segmentation Labeling Tool")
    image_folder = "C:\\Users\\User\\Desktop\\samle"  
    image_paths = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.endswith(".jpg")]
    app = SegmentationLabelingTool(root, image_paths)
    root.mainloop()

if __name__ == "__main__":
    main()
