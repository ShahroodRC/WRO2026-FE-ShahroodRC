<!------------------------------------------------------------------->
<!--                     ShahroodRC – WRO 2026                     -->
<!------------------------------------------------------------------->

<div align="center">

<img src="pictures/shahroodrc-logo.jpg" alt="ShahroodRC logo" width="80%"/>

**ShahroodRC** – *Future Engineers 2026*  
🏆 **1st Place – Iran National WRO 2025**  
🌍 **Heading to Isfahan National Final (26-28 Nov 2025)**  
A fully autonomous LEGO EV3 robot with vision-based obstacle avoidance and precision navigation.

![Status](https://img.shields.io/badge/Status-Competition%20Ready-brightgreen?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-LEGO%20EV3%20%2B%20Python-blue?style=flat-square)
![Team](https://img.shields.io/badge/Team%20Size-3%20Students-orange?style=flat-square)

**📱 Connect with us:**
[![Instagram](https://img.shields.io/badge/Instagram-%23E4405F.svg?style=for-the-badge&logo=Instagram&logoColor=white)](https://instagram.com/shahroodrc)
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=YouTube&logoColor=white)](https://youtube.com/@shahroodrc)
[![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ShahroodRC)

</div>

---

## 🎯 Key Features
| Feature | Details |
|---------|---------|
| 🤖 **Platform** | LEGO EV3 Mindstorms with Python (ev3dev) |
| 👁️ **Vision System** | Pixy 2.1 camera (60 fps, real-time obstacle detection) |
| 🧭 **Navigation** | Dual ultrasonic sensors + color sensor for precision wall-following |
| ⚡ **Performance** | 90% success rate in 50+ test runs; completes challenges in <2min |
| 🔧 **Custom Parts** | 3D-printed Pixy 2.1 mount for optimal positioning |
| 📦 **Components** | All standard LEGO pieces (100% WRO-compliant) |

---

## The Meaning Behind ShahroodRC

ShahroodRC blends "Shahrood" (our hometown in Iran, symbolizing resilience like its mountains) with "RC" (Robotics Club). Inspired by the story of iteration, teamwork, and turning "what if" into "we did it." Behind the code and gears? The quiet support of families – our real "power source," fueling late nights and breakthroughs. ShahroodRC isn't just a robot; it's proof that passion and persistence lead to a global stage.

---

## Table of Contents

- [👥 The Team](#-the-team)
- [🏆 National Championship Victory](#-national-championship-victory)
- [🎯 Mission Overview for WRO Future Engineers Rounds](#-mission-overview-for-wro-future-engineers-rounds)
- [📸 Pictures](#-pictures)
- [🎬 Videos](#-videos)
- [📱 Randomizer App](#-randomizer-app)
- [🔄 Our Path – Platform Evolution](#-our-path--platform-evolution)
- [🔄 Design Evolution & Iteration History](#-design-evolution--iteration-history)
- [📊 Performance Metrics & Statistics](#-performance-metrics--statistics)
- [🤖 Robot Components Overview](#-robot-components-overview)
- [💻 Code For Each Component](#-code-for-each-component)
    - [🔄 Drive Motor Code](#-drive-motor-code)
    - [🎯 Steering Motor Code](#-steering-motor-code)
    - [📷 Pixy Camera Code](#-pixy-camera-code)
    - [🌈 Color Sensor Code](#-color-sensor-code)
    - [💡 LED Indicator Code](#-led-indicator-code)
    - [📏 Ultrasonic Sensor Code](#-ultrasonic-sensor-code)
    - [🔘 Button Control Code](#-button-control-code)
    - [⚡ Main Control Flow](#-main-control-flow)
- [🚗 Mobility Management](#-mobility-management)
    - [1. 📍 Introduction to Mobility System](#1--introduction-to-mobility-system)
    - [2. ⚙️ Motors and Actuators](#2-️-motors-and-actuators)
    - [3. 📡 Sensor Integration for Mobility](#3--sensor-integration-for-mobility)
    - [4. 🎮 Mobility Control Algorithms](#4--mobility-control-algorithms)
    - [5. ⚡ Energy Management for Mobility](#5--energy-management-for-mobility)
    - [6. 🔗 System Integration for Mobility](#6--system-integration-for-mobility)
    - [7. 🧪 Testing and Optimization](#7--testing-and-optimization)
    - [8. ✅ Conclusion](#8--conclusion)
- [⚡ Power and Sense Management](#-power-and-sense-management)
    - [1. 🔋 Power Supply and Distribution](#1--power-supply-and-distribution)
    - [2. 📊 Power Consumption Overview](#2--power-consumption-overview)
    - [3. 📡 Sensor Architecture and Management](#3--sensor-architecture-and-management)
    - [4. 🔗 Wiring and Safety](#4--wiring-and-safety)
    - [5. 🔍 Diagnostics and Monitoring](#5--diagnostics-and-monitoring)
    - [6. ⚙️ Optimization Techniques](#6-️-optimization-techniques)
    - [7. ✅ Conclusion](#7--conclusion)
- [🚧 Obstacle Management](#-obstacle-management)
    - [🏁 Qualification Round (Open Challenge)](#-qualification-round-open-challenge)
    - [🏆 Final Round with Obstacle Avoidance (Obstacle Challenge)](#-final-round-with-obstacle-avoidance-obstacle-challenge)
- [🏗️ Robot Assembly Guide](#️-robot-assembly-guide)
- [🛠️ Software Setup & Installation](#️-software-setup--installation)
- [🔧 Sensor Calibration Guide](#-sensor-calibration-guide)
- [🔴 Problems and Solutions](#-problems-and-solutions)
- [💰 Cost Report](#-cost-report)
- [📁 Repository Structure](#-repository-structure)
- [🤝 Contributing & Support](#-contributing--support)
- [📖 License](#-license)

---

## 👥 The Team

We are the ShahroodRC team, a group of dedicated students from Iran with a passion for robotics, electronics, and programming. Our goal is to design an innovative robot for the WRO 2026 Future Engineers category, leveraging technical skills and collaboration to tackle complex challenges.

### 👨‍💼 Sepehr Yavarzadeh
- **Role**: Project Manager and Software Engineer
- **Age**: 17
- **Description**: Third-time WRO participant, 3rd place in 2025 Robo Mission. Passionate about programming, physics, and math. Enjoys piano and tennis.
- **Contact**: sepehryavarzadeh@gmail.com
- **Links**: [GitHub](https://github.com/Sepehryy) | [Instagram](https://www.instagram.com/sepehr.yavarzadeh/) | [LinkedIn](https://www.linkedin.com/in/sepehr-yavarzadeh-9643252a3/)

### 👨🏼‍🔧 Nikan Bashiri
- **Role**: Mechanical and Electronics Specialist
- **Age**: 18
- **Description**: Advanced LEGO robotics instructor with 5 WRO national finals experience. Expertise in mechanical/electronic systems and LEGO design.
- **Contact**: nikanbsr@gmail.com
- **Links**: [Instagram](https://www.instagram.com/nikanbsr/)

### 🧑‍💻 Amirparsa Saemi
- **Role**: Lead Developer and Algorithm Designer
- **Age**: 20
- **Description**: Third-year WRO competitor, professional ping-pong player. Studying computer science, passionate about math, physics, and programming.
- **Contact**: amirparsa.saemi2021@gmail.com
- **Links**: [Instagram](https://www.instagram.com/hotaru_tempest/)

### 👨🏻‍🏫 Ali Raeesian
- **Role**: Coach
- **Age**: 25
- **Description**: B.Sc. in Computer Engineering, pursuing M.Sc. in Computer Science. Former WRO competitor (2016 global finals). Specializes in game development.
- **Contact**: raeesianali@gmail.com
- **Links**: [GitHub](https://github.com/SheykhAlii) | [Instagram](https://www.instagram.com/ali_raeesiian/)

### 👨🏻‍🏫 Hossein Bagheri
- **Role**: Manager
- **Age**: 51
- **Description**: Founder of Shahrood's educational LEGO institute.
- **Links**: [Instagram](https://www.instagram.com/ho.bagheri/)

### Team Photos
| Sepehr Yavarzadeh | Nikan Bashiri | Amirparsa Saemi | Ali Raeesian | Hossein Bagheri |
|-------------------|---------------|-----------------|--------------|-----------------|
| <img src="t-photos/Sepehr-Yavarzadeh.jpg" alt="Sepehr Yavarzadeh" width="140" height="187"> | <img src="t-photos/Nikan-Bashiri.jpg" alt="Nikan Bashiri" width="140" height="187"> | <img src="t-photos/Amirparsa-Saemi.jpg" alt="Amirparsa Saemi" width="140" height="187"> | <img src="t-photos/Ali-Raeesian.jpg" alt="Ali Raeesian" width="140" height="187"> | <img src="t-photos/Hossein-Bagheri.jpg" alt="Hossein Bagheri" width="140" height="187"> |

<div align="center">
<table>
<tr>
<td align="center">
<img src="t-photos/team.jpg" alt="ShahroodRC" width="220"><br>
<p>The ShahroodRC Team</p>
</td>
<td align="center">
<img src="t-photos/team-funny.jpg" alt="Fun Team Moment" width="220"><br>
<p>Fun Team Moments 🎉</p>
</td>
</tr>
</table>
</div>

> In this project, we aimed to combine creativity, teamwork, and technical knowledge to build an efficient robot for the challenges of WRO 2026.

---

## 🏆 National Championship Victory & International Success

### 2025 National Championship
ShahroodRC secured **1st Place** at the Iran National WRO 2025 Competition (August 2025, Rasht), earning qualification for the WRO 2025 International Final.

### 2025 International Final – Singapore
Competing in the World Robot Olympiad 2025 (November 26–28, Singapore), ShahroodRC achieved:
- ✅ **Full Score** in Open Challenge
- ✅ **Full Score** in Obstacle Challenge
- 🌍 **12th Place Globally**

### 2026 National Qualifiers
Currently preparing for the **Iran National WRO 2026 Qualifying Round** (July 2026, Tehran) to qualify for WRO 2026 International Final.

### Gallery
<div align="center">
<table>
<tr>
<td align="center" width="200">
<img src="t-photos/Shahrood_RC_with_medals.jpg" alt="Gold Medal 2025" width="160"><br>
<p><strong>National Championship Gold Medal</strong><br>2025, Rasht</p>
</td>
<td align="center" width="200">
<img src="t-photos/Shahrood_RC_in_national_competition.jpg" alt="Singapore 2025" width="160"><br>
<p><strong>International Final</strong><br>2025, Singapore</p>
</td>
</tr>
</table>
</div>

---



## 🤝 Contributing & Support

This project is **open-source** and welcomes:
- 🐛 **Bug reports** – Found an issue? Let us know!
- 💡 **Suggestions** – Have ideas for improvement? Share them!
- 📚 **Documentation improvements** – Help make it clearer!

### Quick Links
- 📧 **Email**: sepehryavarzadeh@gmail.com (Project Manager)
- 🌐 **Instagram**: [@shahroodrc](https://instagram.com/shahroodrc)
- 📹 **YouTube**: [ShahroodRC Channel](https://youtube.com/@shahroodrc)

---

## Mobility & Mechanical Design — تحرک و طراحی مکانیکی

هدف این بخش ارائهٔ طراحی مکانیکی و راه‌حل‌های تحرکی ربات است تا معیارهای قضاوت WRO را به‌صورت کامل پوشش دهد. در قدم‌های بعدی هر زیرعنوان را به‌صورت دقیق و با داده/تصاویر/محاسبات تکمیل خواهیم کرد.

### 1. معرفی کلی (Overview)
- خلاصه‌ای از فلسفهٔ طراحی، اهداف عملکردی (پایداری، سرعت، دقت) و محدودیت‌ها (قوانین WRO، وزن، اندازه).

### 2. شاسی و معماری ساختاری (Chassis & Structural Design)
- نوع شاسی (قاب‌بندی، باز/بسته)، نقاط اتصال حیاتی، تحلیل استحکام کلی و دلایل انتخاب هندسه.

### 3. سامانهٔ محرک و گیربکس (Drive System & Gear Ratios)
- موتورهای استفاده‌شده، نسبت‌های دنده‌ای، محاسبات توان و گشتاور، مزایای انتخاب شده نسبت به جایگزین‌ها.

### 4. چرخ‌ها، کشش و انتخاب مواد (Wheels, Traction & Materials)
- انتخاب نوع چرخ، قطر و پهنا، پوشش لاستیکی، تحلیل کشش و مقاومت لغزش، انتخاب مواد برای قطعات بحرانی.

### 5. سیستم فرمان‌دهی و تعلیق (Steering & Suspension)
- نوع فرمان (دوچرخ، چهارچرخ، آرنجی)، مکانیزم تعلیق (در صورت وجود)، نحوهٔ حفظ تماس با زمین در سطوح نامساوی.

### 6. یکپارچه‌سازی حسگرها و مونتاز (Sensor Mounting & Integration)
- محل نصب دوربین/سنسورها، معیارهای زاویه/ارتفاع، روش‌های ثابت‌سازی و کاهش نویز مکانیکی.

### 7. توزیع بار و پایداری (Load Distribution & Stability)
- مرکز جرم، محدودهٔ پایدار، تحلیل واژگونی و تغییرات طراحی برای افزایش پایداری در مانورها.

### 8. نصب، تولید و قطعه‌سازی (Assembly & Fabrication)
- دستورالعمل کلی مونتاژ، قطعات سفارشی (3D-printed)، پیچ‌ها/برآمدگی‌ها و نکات مقاوم‌سازی.

### 9. ایمنی مکانیکی و رعایت قوانین (Mechanical Safety & Compliance)
- جلوگیری از قطعات تیز/آزاد، ایمنی مدارهای متصل به مکانیک، انطباق با قوانین WRO دربارهٔ قطعات و وزن.

### 10. تست، اعتبارسنجی و معیارهای عملکرد (Testing & Validation)
- برنامهٔ آزمایش (تست‌های استاتیک و دینامیک)، معیارهای گذر (سرعت، دقت مسیر، توانایی عبور از موانع) و نتایج نمونه.

### 11. بهینه‌سازی و ملاحظات طراحی (Optimization & Trade-offs)
- بررسی گزینه‌های جایگزین، نحوهٔ بهبود بازده و کاهش وزن بدون افت عملکرد.

### 12. چک‌لیست امتیازدهی برای داوران (Judge-Focused Checklist)
- مواردی که باید ارائه و مستندسازی شوند تا حداکثر امتیاز مکانیک و تحرک کسب شود (مستندات، محاسبات، تصاویر، ویدیوهای تست).

### منابع و مراجع
- محل قرارگیری نقشه‌ها، CAD، عکس‌های اسمبلی و فایل‌های محاسباتی (لینک‌ها و توضیحات).

---

## 📖 License
This project is licensed under the **MIT License**, allowing free use, modification, and distribution with proper attribution. See the [LICENSE](LICENSE) file for full details.

---

<div align="center">

**Built with ❤️ by ShahroodRC Team**

🚀 Representing Iran at WRO 2025 International Final in Singapore 🌍

See you in Singapore!

© 2025 ShahroodRC – All rights reserved.

</div>