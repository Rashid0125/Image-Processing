import easyocr
import cv2

reader = easyocr.Reader(['hi', 'en'], gpu=False)  #Hindi, telugu, and English
for img_name in os.listdir("/content/drive/MyDrive/task-3"):    #target folder
    if img_name.endswith(".jpg") or img_name.endswith(".png"):
    print(img_name)
    img = cv2.imread(img_name)
    results = reader.readtext(img, detail=1, paragraph=False) 
    for (bbox, text, prob) in results:

        #Define bounding boxes
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))

        #Remove non-ASCII characters to display clean text on the image (using opencv)
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()

        #Put rectangles and text on the image
        cv2.rectangle(img, tl, br, (0,204,204), 2)
        cv2.putText(img, text, (tl[0], tl[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 102, 0), 2)
        cv2.imwrite(f"/content/drive/MyDrive/task-3/gen_results/{img_name}",img)  #images append to result folder