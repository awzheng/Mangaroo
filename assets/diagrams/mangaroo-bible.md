```eraser.io
title Mangaroo Story Bible Logic
direction right

Input PDF [shape: oval, icon: file-pdf, color: blue]

Text [color: orange] {
  Page 1 [shape: oval, icon: text]
  Page 2 [shape: oval, icon: text]
  Page n-1 [shape: oval, icon: text]
  Page n [shape: oval, icon: text]

}

Images [color: green] {
  Image 1 [shape: oval, icon: image]
  Image 2 [shape: oval, icon: image]
  Image n-1 [shape: oval, icon: image]
  Image n [shape: oval, icon: image, color: green]
}

Input PDF > Page 1
Page 1 > Page 2
Page 2 > Page n-1: ...
Page n-1 > Page n

Page 1 > Image 1
Page 2 > Image 2
Page n-1 > Image n-1
Page n > Image n

Image 1 > Image 2
Image 2 > Image n-1: ...
Image n-1 > Image n
```