# 2019-nCoV
<p align = "center">
  <a href = "https://github.com/mathors/2019-nCoV">
    <img src="https://img.shields.io/badge/Language-Python-brightgreen.svg">
  </a>
  <a href = "https://github.com/mathors/2019-nCoVe">
    <img src = "https://img.shields.io/badge/Compiler-VsCode-blue.svg">
  </a>
  <a href = "https://wmathor.com/" target = "_blank">
    <img src = "https://img.shields.io/badge/Blog-wmathor-orange.svg">
  </a>
</p>

This repo holds the code for crawling the **latest news** on the pneumonia virus from the Internet

[中文](https://github.com/wmathor/2019-nCoV/blob/master/README-cn.md) | [English](https://github.com/wmathor/2019-nCoV)

The content of the crawling includes the number of confirmed cases, the number of suspected cases, the progress of relevant research (source of infection, route of transmission, etc.), the number of infected cases in various provinces and the latest 3 real-time news

If you don't see your province in an infected province, it may be because no cases have been found, but that doesn't mean you can let your guard down

It may be faster for domestic users to [download](https://www.qsc.zju.edu.cn/box/-54707039) EXE files through this link

----
### :art:2020-02-03 New Program
The function of 2019-ncov-timer. py program is to crawl the data at 0:00 am every day, and save it in the current sheet with the date of the day as the sheet name. The program was written to make it easier for researchers to analyze data

Please read the following notes carefully

1. You need to make sure that when the program is running, 2019- ncov.xlsx this Excel file is closed
2. It needs to be run before 0 a.m. every day to make sure the program is running until it says, "file was written successfully."
3. Run directly, and the Excel directory generated is the same as the directory where the program runs

Part of the data in Excel are as follows:

![](https://s2.ax1x.com/2020/02/03/1UMBgf.png)

### 2020-1-29 V2.3 update

- Fixed some bugs caused by changes in web source code

### 2020-1-28 V2.2 update

- Added the situation of the outbreak abroad
- Dxiang doctor website source code modification has been adapted

### 2020-1-25 V2.1 update
- Updated crawler location elements
- Removed the imformation about me

### 2020-1-24 V2.0 update

- Updated crawler location elements
- Updated province information display, now in tabular form
- Support to search for relevant information in a province
- The lilac doctor data interface was used

----

### :rocket:ABOUT

This project was written by me after staying up late for 2 hours in the evening. I just hope to call on all of you to give full play to your strengths, use what you have learned and do something within your capacity for the prevention and control of the epidemic. You can say that my project is rubbish, but please don't say that I am trying to make a show. No Chinese would make a show of this kind of thing

### :tada:TODO

My power is limited, you can help optimize the code to make it simpler, or you can do some awesome projects, such as data visualization of epidemic transmission. I will also continue to improve the project, welcome to ask more questions. Thanks

I'll soon deploy the data I've crawled to the server as json, so you can call it

![](https://s2.ax1x.com/2020/01/28/1KNPUK.gif)
