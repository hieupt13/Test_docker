# brazil-ceaf-api
Data collector for http://www.portaltransparencia.gov.br/download-de-dados/ceaf

This project will collect data from the website above. The data appears as a csv file inside a ZIP file that updates infrequently.

The file itself is http://www.portaltransparencia.gov.br/download-de-dados/ceaf/20201102 (csv file compressed with zip) and the link is built using javascript information on the collection page, using the year, month and day on the arquivos.push line.
```
<!-- Inclusao dos arquivos JavaScript definidos em cada view -->
    <script type="text/javascript" src="/static/js/portal/download-planilhas.js?v=1.45.0"></script>
<script>

    var arquivos = [];

        arquivos.push({"ano" : "2020", "mes" : "11", "dia" : "02", "origem" :  "Expulsoes"});

    var url = springUrl + "download-de-dados/ceaf/";
    var download = new DownloadPlanilhas("ceaf", arquivos, "DIA", url);
    download.criarLinksIniciais();
</script>
```

The project has two parts:
1. Collection part, we need a python script that does a request.get to http://www.portaltransparencia.gov.br/download-de-dados/ceaf, gets the year, month and day for the archive; then check the local database to verify whether that data has been imported already. If it has, stop processing. If the file is new, then assemble the link to the zip file, download the zip file, then uncompress the csv file inside it and import it on the database. The database will be a single table with the same columns as the csv file with an additional column called "file_import" which will contain the yyyymmdd value of the imported file.

2. An API - similar to the offshore leaks API that will allow to search for a term on only the latest imported file.  This can be done by selecting the highest value of the file_import column with the MAX() SQL function and then select ... where name like '%%s%; on those results.

