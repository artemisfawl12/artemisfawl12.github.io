from django.shortcuts import render
#import matplotlib.pyplot as plt
import requests
from urllib import parse
from bs4 import BeautifulSoup as bs

chaminfo=requests.get('http://ddragon.leagueoflegends.com/cdn/10.11.1/data/ko_KR/champion.json')
iteminfo=requests.get('http://ddragon.leagueoflegends.com/cdn/10.11.1/data/ko_KR/item.json')

def score_view(request):
    return render(request, 'score/score_view.html')

def search_result(request):
    if request.method=="GET":
        summonerName=request.GET.get('search_text')
        summoner_exist = True
        sum_result = {}
        solo_tier = {}
        team_tier = {}
        store_list = []
        game_list ={}
        game_list2 = []
        developapikey = 'RGAPI-267a6b0a-3a15-496a-a646-19d6ea356027'
        encodingName=parse.quote(summonerName)
        apiurl='https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+encodingName #accountid 받아오는 주소.
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Accept-Language": "ko,en-US;q=0.9,en;q=0.8",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": developapikey
        }
        res=requests.get(apiurl,headers=headers)

        data=res.json()
        accountId=data['accountId']
        Id=data['id']
        ##GET /lol/match/v4/matchlists/by-account/{encryptedAccountId}
        ##Get matchlist for games played on given account ID and platform ID and filtered using given filter parameters, if any.
        chamdata=chaminfo.json()
        t=chamdata['data']
        keylis=[]
        namelis=[]
        for i in t.values():
            keylis.append(i['key'])
            namelis.append(i['name'])

        keynamedict={}

        for i in range(len(keylis)):
            keynamedict.setdefault(keylis[i],namelis[i])
        ##key, name dictionary spawned.

        apiurl='https://kr.api.riotgames.com/lol/match/v4/matchlists/by-account/'+accountId
        res=requests.get(apiurl,headers=headers)
        matchlistdata=res.json()
        championlist=[]
        lanelist=[]
        gameIdlist=[]
        for game in matchlistdata['matches']:
            championlist.append(game['champion'])
            lanelist.append(game['lane'])
            gameIdlist.append(game['gameId'])

        gamenumb=len(gameIdlist)

        strchamplist=[]
        for i in range(gamenumb):
            strchamplist.append(keynamedict[str(championlist[i])])
        for i in range(gamenumb):
            print("game id: "+str(gameIdlist[i])+' YR champ: '+strchamplist[i])
        ##여기까지는 챔피언 이름이랑 게임 Id를 출력. 대부분의 list에는 그냥 게임 순서대로 받아다 들어가게 되어있음.
        ##developapikey는 매번 바꿔줘야함. 라이엇에 메일보내서 승인받으면 영구적인거 받기는 함.
        ##이제 i에 대해서 데이터 받아와야 함. 받아다가 경치 차이라도 보여주면서... ㅇㅋ? 시간당 경치 차이. 우물에 계속 있는놈이라도 잡아낼수 있게
        ##gameId를 gameIdlist에 넣어놨으니까 여러개 뺴다써야하는데 일단 0일때에 대해서만 코드 만든것.
        #matchnum=int(input('YR wanted matchnum'))
        matchnum=0
        matchres={}
        for matchnum in range(10):
            apiurl='https://kr.api.riotgames.com/lol/match/v4/timelines/by-match/'+str(gameIdlist[matchnum])
            res=requests.get(apiurl,headers=headers)
            MatchTimelineDto=res.json()


            apiurl='https://kr.api.riotgames.com/lol/match/v4/matches/'+str(gameIdlist[matchnum])
            res=requests.get(apiurl,headers=headers)
            mthdata=res.json()
        #여기까지 데이터는 다 받아옴.
        #summonerName parsing.
            tempName=summonerName.split()
            UserNametemp=''
            for i in tempName:
                UserNametemp+=i
                UserName=UserNametemp.lower()

                playerdata=mthdata['participantIdentities']
                print()
            for i in playerdata:
                print(i['player']['summonerName'])
                tempserverName=i['player']['summonerName'].split()
                ServerNametemp=''
                for temp in tempserverName:
                    ServerNametemp+=temp
                ServerName=ServerNametemp.lower()
                if(ServerName==UserName):
                    thisparticId=i['participantId']


            print('\n'+ str(thisparticId))#이거 띄어쓰기랑 대소문자 안맞으면 안나와버림..
            ##thisparticId: 입력받은 플레이어의 데이터상 아이디.
            ParticipantDto=mthdata['participants']

            for idfind in ParticipantDto:
                if(thisparticId==idfind['participantId']):
                    ParticipantTimelineDto=idfind['timeline']
                    ParticipantStatsDto=idfind['stats']

            #print(ParticipantTimelineDto)
            MatchFrameDto=MatchTimelineDto['frames']#이건 list

            temptime=0
            timenum=0
            trolltime=0
            for i in MatchFrameDto:
                for j in range(1,11):
                    if(i['participantFrames'][str(j)]['participantId']==thisparticId):
                        try:
                            x=i['participantFrames'][str(j)]['position']['x']
                            y=i['participantFrames'][str(j)]['position']['y']
                            if(x<600 and y<600):
                                trolltime+=1
                            timenum+=1
                            #plt.plot(x,y,'ro')
                            temp=i['timestamp']
                        except:
                            print('game ended')

            measure=trolltime/timenum



            #plt.draw()
            #fig=plt.gcf()
            #fig.savefig('m'+str(matchnum)+'.png',dpi=fig.dpi)
            matchres.setdefault(matchnum,round(measure,4))



        return render (request, 'score/search_result.html', {'matchres': matchres})








# Create your views here.
