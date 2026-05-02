# AI-Based Cheating Detection System (Prototype)

## What this prototype does
- Detects multiple faces in frame (possible collusion)
- Detects head turns (left/right) using MediaPipe FaceMesh
- Detects mouth open (simple talking heuristic)
- Optionally detects objects (requires MobileNet-SSD model files — see below)

## How to set up

1. Install Python 3.8+ (3.10 recommended).
2. (Optional but recommended) Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate    # Linux / macOS
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Optional (object detection / mobile detection):
   Download MobileNet-SSD files and put them into the `models/` folder:
    - MobileNetSSD_deploy.prototxt
    - MobileNetSSD_deploy.caffemodel
   You can find them (example repo): https://github.com/chuanqi305/MobileNet-SSD
   If you don't add them, mobile detection will be disabled but the rest will work.

5. Run:
   ```
   python main.py
   ```

6. Controls:
   - Press 'q' to quit.

## Notes & Improvements
- This is a prototype: lighting, camera angle, and occlusions affect accuracy.
- For production: use a trained object detector for phones, better mouth/voice detection, logging, GUI, and server-side storage.
- See VTU project report template for documenting algorithms and testing.
