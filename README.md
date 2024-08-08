# pa-calc
Collection of tools to compute physical activity intensity levels in infants using accelerometers.

Versions:
- python-gui: Needs python and relevant python libraries installed
- windows-x64: Executable application for Windows running on Intel 64-bit processors [download link] *under development*
- macos-x64: Executable application for MacOS running on Intel 64-bit processors [download link] *under development*
- macos-aarch64: Executable application for MacOS running on Apple Silicon processors [download link] *under development*

**Notice: We are in the process of updating the code.**
  
Library requirements for those running it on Python:
- tkinter
- numpy
- pillow version 9.2.0 or higher
- numpy version 1.23.3 or higher
- pytz version 2022.1 or higher
- tkinter version 8.6 or higher (is already built into Python)
- datetime (is already built into Python)
- time (is already built into Python)

Based on the paper:

Mustafa A. Ghazi, Judy Zhou, Kathryn L. Havens, and Beth A. Smith. Accelerometer Thresholds for Estimating Physical Activity Intensity Levels in Infants: A Preliminary Study. *Sensors*, 24(14):4436, 2024. URL: [https://www.mdpi.com/1424-8220/24/14/4436](https://www.mdpi.com/1424-8220/24/14/4436)

Abstract:

Lack of physical activity (PA) at a young age can result in health issues. Thus, monitoring PA is important. Wearable accelerometers are the preferred tool to monitor PA in children. Validated thresholds are used to classify activity intensity levels, e.g., sedentary, light, and moderate-to-vigorous, in ambulatory children. No previous work has developed accelerometer thresholds for infancy (pre-ambulatory children). Therefore, this work aims to develop accelerometer thresholds for PA intensity levels in pre-ambulatory infants. Infants (n = 10) were placed in a supine position and allowed free movement. Their movements were synchronously captured using video cameras and accelerometers worn on each ankle. The video data were labeled by activity intensity level (sedentary, light, and moderate-to-vigorous) in two-second epochs using observational rating (gold standard). Accelerometer thresholds were developed for acceleration and jerk using two optimization approaches. Four sets of thresholds were developed for dual (two ankles) and for single-worn (one ankle) accelerometers. Of these, for a typical use case, we recommend using acceleration-based thresholds of 1.00 m/s to distinguish sedentary and light activity and 2.60 m/s to distinguish light and moderate-to-vigorous activity. Acceleration and jerk are both suitable for measuring PA.

*Keywords:* physical activity intensity; wearable accelerometer; infant; threshold; validation
