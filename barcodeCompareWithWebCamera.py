import cv2

from pyzbar.pyzbar import decode

# SequenceMatcher computes a similarity 

from difflib import SequenceMatcher


# You can think of this as the 'Manifest', just that this is not in a USB

CATALOG = [
    "079400471885",
    "888853000589",
     "02289111",  
]


def similarity(a: str, b: str) -> float:
    """
    Return similarity ratio between two strings on [0..1].
    Uses difflib.SequenceMatcher; great for small mistakes or partial mismatches.
    """
    return SequenceMatcher(None, a, b).ratio()


def best_match_for(code: str, catalog: list[str]) -> tuple[str | None, float]:
    """
    Find the most similar string to 'code' inside 'catalog'.
    Returns a tuple: (best_catalog_item_or_None, best_similarity_score).
    If catalog is empty, returns (None, -1.0).
    """
    best_item, best_score = None, -1.0
    for item in catalog:
        s = similarity(code, item)
        if s > best_score:
            best_item, best_score = item, s
    return best_item, best_score



def main():
   
    cap = cv2.VideoCapture(0)

    
    cap.set(3, 640)  
    cap.set(4, 480)  

    
    if not cap.isOpened():
        print(" Could not open camera. Try a different index (1, 2) or close other apps using it.")
        return

    print(" Point a barcode at the camera. Press 'q' to quit.")

    
    while True:
        
        ret, frame = cap.read()
        if not ret:
            # If we failed to get a frame, stop the loop.
            print(" Could not read a frame from the camera.")
            break

        
        for sym in decode(frame):
            
            code = sym.data.decode("utf-8").strip()
            if not code:
                
                continue

            # Compare the scanned code to your catalog and get the best match + score.
            match, score = best_match_for(code, CATALOG)

            # Decide if it's a "match" based on a threshold 
            THRESHOLD = 0.75
            is_match = score >= THRESHOLD
            status_text = " MATCH" if is_match else " NO MATCH"

            
            print(f"Scanned: {code} | Best: {match} | Sim={score:.2f} | {status_text}")

            
            # sym.polygon gives corner points around the detected code.
            pts = [(p.x, p.y) for p in sym.polygon]
            # Draw lines between consecutive corners to make a box.
            for i in range(len(pts)):
                cv2.line(frame, pts[i], pts[(i + 1) % len(pts)], (0, 255, 0), 2)

            
            top_left = (sym.rect.left, max(0, sym.rect.top - 10))
            cv2.putText(
                frame,
                f"{status_text} ({score:.2f})",
                top_left,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),  # green text
                2,
                lineType=cv2.LINE_AA,
            )

        
        cv2.imshow("Barcode Scanner", frame)

        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()
