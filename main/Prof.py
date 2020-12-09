
#キャラクターのプロフィール

char_prof = [

	"白上フブキ\n白髪ケモミミの女子高生。恥ずかしがり屋であ\nり、おとなしめな性格だけれど、実は人と話すの\nが好きで、構ってもらえると喜ぶ。\n公式の紹介分より ",
	
	"戌神ころね\n都会にあるパン屋さんにいる犬。店番をしながら\n空いた時間にゲームをしている。\n公式の紹介分より",
	
	"湊あくあ\nマリンメイド服のバーチャルメイド。本人は頑張\nっているがおっちょこちょいでドジっ子。\n公式の紹介分より",
	
	"兎田ぺこら\n寂しがり屋なうさ耳の女の子。にんじんをこよな\nく愛し、いつでも食べられるように持ち歩いている。\n公式の紹介分より",
	
	"桐生ココ\n人間の文化に興味を持ち、異世界から日本に語学\n留学中の子どものドラゴン。\nで、気合で人間の姿を保っている。\n公式の紹介分より",
	
	"宝鐘マリン\n宝石、宝、お金が大好きで、海賊になって宝を探\nすのが夢。海賊船を買うのが目標で今は陸で",
	
	"夏色まつり\nチア部の新入生。明るく元気で人懐っこい性格で\nあり誰とでもすぐに仲良くなれて、友達も多い。\n祭りやイベントなど楽しいことが好き。\n公式の紹介分より",
	
	"赤井はあと\n生意気な後輩。普段はツンツンしているが仲良く\nなった相手には甘えたりする。赤いリボンとハー\nトが好きで、髪や服によくつけている。\n公式の紹介分より",
	
	"白銀ノエル\nおっとりしているが、なんでも筋力でどうにかす\nる物騒な面を持つ ゆるふわ脳筋女騎士。強さに憧\nれるあまり、つよつよな人達が集まるVTuber界に\n武者修行にきた。\n公式の紹介分より",
	
	"潤羽るしあ\n人前に出ることが苦手な魔界学校に所属のネクロ\nマンサー(死霊使い)の少女。\nひとりぼっちが嫌なので死霊や屍とおしゃべりを\nしている。"
	
]

#キャラクターの画像のパス

img_pass = [

	".\char_imgs\sirakami.png",
	".\char_imgs\inugami.png",
	".\char_imgs\minato.png",
	".\char_imgs\susada.png",
	".\char_imgs\kiryu.png",
	".\char_imgs\housyou.png",
	".\char_imgs\snatuiro.png",
	".\char_imgs\sakai.png",
	".\char_imgs\sirogane.png",
	".\char_imgs\suruha.png",
	
]

chr_url = [
'https://www.hololive.tv/portfolio/items/336378',
'https://www.hololive.tv/portfolio/items/336401',
'https://www.hololive.tv/portfolio/items/336383',
'https://www.hololive.tv/portfolio/items/336270',
'https://www.hololive.tv/portfolio/items/360918',
'https://www.hololive.tv/portfolio/items/336351',
'https://www.hololive.tv/portfolio/items/336381',
'https://www.hololive.tv/portfolio/items/336380',
'https://www.hololive.tv/portfolio/items/336353',
'https://www.hololive.tv/portfolio/items/336265'
]

def prof_return(char_number):
	return char_prof[char_number]

def img_return(char_number):
	return img_pass[char_number]

def url_return(char_number):
	return chr_url[char_number]



