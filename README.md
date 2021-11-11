# RingVideoTimeLaps
Downloads Ring.com camera video and utilizes ffmpeg to create a time laps video

# setup python
```
pyenv virtualenv 3.7.0 Ring
pyenv local Ring
pip install requirements.txt
```

# install ffmpeg
https://formulae.brew.sh/formula/ffmpeg
```
brew install ffmpeg
```

# run
```
python Ring.py
```

Run ffmpeg
```
cd images
ffmpeg -framerate 30 -pattern_type glob -i '*.jpg' -c:v libx264 -pix_fmt yuv420p out.mp4
```

# Example Final Product
https://www.youtube.com/watch?v=5Vl4Oke4DcA