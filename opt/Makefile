run:
	screen -U python3 scheduler-v3.py
# -U はUTF-8のいみ

ls:
	screen -ls

enter:
	screen -rU $(screen -ls | grep -o '[0-9]\+' | sed -n '1p')

example:
	@echo '起動後の抜け方: ctl+a -> ctl+dでscreenを抜ける'
	@echo '復帰方法:screen -rU $(screen -lsで取得できる番号)'
