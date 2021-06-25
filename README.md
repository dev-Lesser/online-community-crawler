## online community crawler

- 일베
- 클리앙
- 디씨
- 펨코 -> 로봇 감지 기능이 있어 ip ban 있어, 제외시킴
- 인벤
- 엠팍
- 뽐뿌

위 사이트에 대해 이준석 관련 게시물을 수집합니다.

### running MongoDB
```
docker-compose up -d

```
- db name : online_community
- collection name : community

### 데이터 포맷
- title : 제목
- content : 내용
- date: 작성일자
- vote_up : 추천 수 
- vote_down : 비추천 수 (fmkorea, clien, mlbpark 는 비추천 수가 없어서 default 0, ilbe의 경우 - 음수임)
- url : url 기준 데이터가 없으면 insert 하는 형식
- source : ilbe, dcinside, inven, mlbpark, ppomppu, clien 중 1개
### running Crawler
```bash
cd ./online_community_crawl

python run_crawler.py
```

### trouble shooting (TODO)
- fmkorea의 경우 로봇 감지 빈도가 민감하여서 download delay를 재설정 해야 할 필요가 있음 > 제외 결정
