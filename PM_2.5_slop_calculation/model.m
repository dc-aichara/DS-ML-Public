peaksData1  = ncread('GlobalGWRc_PM25_GL_199801_199812-RH35.nc','PM25');
peaksData2  = ncread('GlobalGWRc_PM25_GL_199901_199912-RH35.nc','PM25');
peaksData3  = ncread('GlobalGWRc_PM25_GL_200001_200012-RH35.nc','PM25');
peaksData4  = ncread('GlobalGWRc_PM25_GL_200101_200112-RH35.nc','PM25');
peaksData5  = ncread('GlobalGWRc_PM25_GL_200201_200212-RH35.nc','PM25');
peaksData6  = ncread('GlobalGWRc_PM25_GL_200301_200312-RH35.nc','PM25');
peaksData7  = ncread('GlobalGWRc_PM25_GL_200401_200412-RH35.nc','PM25');
peaksData8  = ncread('GlobalGWRc_PM25_GL_200501_200512-RH35.nc','PM25');
peaksData9  = ncread('GlobalGWRc_PM25_GL_200601_200612-RH35.nc','PM25');
peaksData10  = ncread('GlobalGWRc_PM25_GL_200701_200712-RH35.nc','PM25');
peaksData11  = ncread('GlobalGWRc_PM25_GL_200801_200812-RH35.nc','PM25');
peaksData12  = ncread('GlobalGWRc_PM25_GL_200901_200912-RH35.nc','PM25');
peaksData13  = ncread('GlobalGWRc_PM25_GL_201001_201012-RH35.nc','PM25');
peaksData14  = ncread('GlobalGWRc_PM25_GL_201101_201112-RH35.nc','PM25');
peaksData15 = ncread('GlobalGWRc_PM25_GL_201201_201212-RH35.nc','PM25');
peaksData16  = ncread('GlobalGWRc_PM25_GL_201301_201312-RH35.nc','PM25');
peaksData17  = ncread('GlobalGWRc_PM25_GL_201401_201412-RH35.nc','PM25');
peaksData18  = ncread('GlobalGWRc_PM25_GL_201501_201512-RH35.nc','PM25');

out1 = cat(18,peaksData1, peaksData2, peaksData3, peaksData4, peaksData5, peaksData6, peaksData7, peaksData8, peaksData9, peaksData10, peaksData11, peaksData12, peaksData13, peaksData14, peaksData15, peaksData16, peaksData17, peaksData18);
%imshow(out1);

year=1:18;
output=zeros(3600,1246);
for i=1:3600
    for j=1:1246
        y=zeros(18,1);
        for k=1:18
            y(k)=out1(i,j,k);
        end
            
        %o=out1(i,j,:);
        mdl = polyfit(year',y,1);
        output(i,j)=mdl(1);
    end
end

imwrite(output,'slope_pm25.png')
imtool(output);