Link CADETS_E3: [https://drive.google.com/drive/u/0/folders/1PHmGELAN7c9qq_Q_bNdGGfoMovhhJa2G](https://drive.google.com/drive/folders/1PHmGELAN7c9qq_Q_bNdGGfoMovhhJa2G?usp=sharing)

Cần cài đặt torch trước khi cài đặt requirement.txt
# PyTorch GPU version
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia


Sửa đường dẫn trong file config.py:
+ raw_dir (dataset)
+ database (tc_cadet3.db có trong thư mục CADETS_E3)
