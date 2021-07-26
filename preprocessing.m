foldername = 'C:\Users\User\Desktop\data_original';                        %mat파일이 있는 폴더로 설정
workspace = foldername;                                                    %워크스페이스 설정(디폴트는 foldername과 같게)
filename = 's'+string(i)+'.mat';
load(filename);                                                            %'foldername 내 mat 파일 

newdata = squeeze(data);                                                   %원본 mat 안의 차원 축소

ppg = newdata(46,:);                                                       %ppg 데이터만 뽑아내기
    %----------필터링------

    %---------------------
tmp = ppg(1,1:8864);                                                       %영상별로 데이터 자르기
velence = labels(1,1);                                                     %레이블 설정
arousal = labels(1,2);
video = 1;
people = 1;
lab = [velence arousal video people];                                      %레이블 뽑아내기
pps = [tmp lab];                                                           %레이블 붙이기

for i = 1:32                                                               %32명에 대한 데이터 모두 진행하기
    if(i~=1)                                                               %1번 파일 진행했으므로, 파일 열기 생략
    filename = 's'+string(i)+'.mat';
    load(filename);

    newdata = squeeze(data);

    ppg = newdata(46,:);
    %----------필터링------

    %---------------------
    end
    for j = 1:40                                                           %피실험자들의 데이터를 영상별로 분류
        if(i==1&&j==1)
            continue;
        end
        
        tmp = ppg(1,1 + (j - 1) * 8864 : j * 8864);
        velence = labels(j,1);
        arousal = labels(j,2);
        video = j;
        people = i;
        lab = [velence arousal video people];
        pps = cat(1,pps,[tmp lab]);
    end
end

save('pps.mat','pps');                                                     %필터링 된 데이터 mat 파일로 저장
