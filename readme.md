<p align="center">
  <img src="images/logo.jpg" width="750" />
</p>

## Project Summary 

This project proposes and implements a mobile device that tracks environmental threats for outdoor athletes in the summer. The proposed device, called AlertAthlete, considers the Wet Bulb Globe Temperature (WBGT), ultraviolet index (UVI), and chance of rain and lightning as the threat indicators. WBGT quantifies the heat stress on the body in direct sunlight and indicates the risk of potential heat stroke. UVI quantifies the intensity of UV radiation, which causes sunburn, and indicates the risk of potential skin cancer. Rain and lightning impact the safety of athletic practice/events. 

AlertAthlete is implemented with a battery-operated RP2040 microcontroller, a batteryless e-ink display, and a real-time clock (RTC). MicroPython code runs through deep sleep cycles with the RTC to periodically download environmental forecasts from the National Oceanic and Atmospheric Administration (NOAA) and OpenWeatherMap. Then, it shows the forecasts and suggested precautions on the e-ink display. AlertAthlete aids athletes to take precautions early for their safety, such as taking breaks in the shades, extra water and sunscreen. 

This project was presented at [PhysTech 2025](https://phystech2025.devpost.com/). It won a [2nd place](https://phystech2025.devpost.com/project-gallery) award.

## Publications

- Hanna Suzuki, "AlertAthletes: A Real Time Alert Tracker for Outdoor Athletes in the Summer," In R. Nagata, H. Suzuki and S. Nagata (eds.), *Innovation in Motion: Technology Hacks from PhysTech 2025*, Chapter 9, pp., Binnovative, September 2025.

## Key Features:

- Downloading and displaying environmental forecasts
- Displaying suggested precautions (WBGT-based activity modification and UVI-based sun protection)
- Easy to use screen transitions with physical buttons
- Saving battery consumption through deep sleep cycles 

https://github.com/user-attachments/assets/80729b33-b0b7-4be8-ba07-94c1bcf11b65

