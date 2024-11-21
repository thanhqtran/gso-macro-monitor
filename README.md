# Vietnam Macroeconomic Monitor

This project aims at providing the most accurate and up-to-date data about the Vietnamese economy.

With the data, you can make fancy figures.

- I scrape the data from GSO (stored in `.xml` format). In total, there are 13 databases.
- I then extract the information from these databases and store them in one single `.json` file.
- To download, see `Release` on the right panel.

**Notes**: We used archived links for now since some of the links are not accessible in real-time.

The archived links contain data until the end of 2023 (National Accounts data until 2023q2).

Data since 2023q2 can be accessed in the [Excel sheets provided by GSO](http://nsdp.gso.gov.vn/index.htm).

## Tiếng Việt

Để tiện cho mục tiêu nghiên cứu, mình viết một số script trên Python để cho máy đọc dữ liệu chính thức từ Tổng cục thống kê GSO.

Với CSDL này, chúng ta có thể vẽ các biểu đồ cơ bản hoặc ước lượng các mô hình vĩ mô.

Hiện nay GSO có 13 CSDL kinh tế, chủ yếu quan tâm đến các dữ liệu vĩ mô theo quý.

Những ai cần dùng có thể tải về toàn bộ data ở mục `Release`.

Do link `SDMX` của GSO không ổn định, nhiều khi không truy cập được nên mình chỉ sử dụng các đường link sao lưu trên Internet Archive ở thời điểm gần nhất (2023/12/31). Riêng dữ liệu về Tài khoản quốc gia có từ 2010q1 đến 2023q2. Dữ liệu từ 2023q2 trở đi có thể truy cập thủ công ở các bảng tính [Excel cung cấp bởi GSO](http://nsdp.gso.gov.vn/index.htm).

Trong tương lai, khi đường link chính ổn định hơn, mình sẽ update `Release` mới.

Phần link gốc không có mô tả ý nghĩa `@INDICATOR`. Ai quan tâm có thể tham khảo ở file `dsbb_indicator_desc.csv`.


---


## Data sources

- Vietnam consolidated macroeconomic data: [DSBB Standard](http://nsdp.gso.gov.vn/index.htm)

- General Statistics Office of Vietnam: [GSO](https://pxweb.gso.gov.vn/pxweb/en/)

- My dataset collection: [thanhqtran/dataset](https://github.com/thanhqtran/dataset)

## Code Reference:

- Real-time routines: [Scheduling Notebook and Script Runs with GitHub Actions](https://towardsdatascience.com/scheduling-notebook-and-script-runs-with-github-actions-cc60f3ac17f2), with [Git Repo](https://github.com/venkatesannaveen/medium-articles).

- [Git-hub Stats real-time visualization](https://github.com/jstrieb/github-stats)

- [Making gif animation plots](https://towardsdatascience.com/basics-of-gifs-with-pythons-matplotlib-54dd544b6f30)
  
## To visualize data structure

- [json viewer](http://jsonviewer.stack.hu/)

- [Code Beautify](https://codebeautify.org)

### Deployed at [Macro Monitor](https://thanhqtran.github.io/macroeconomicmonitor/)
