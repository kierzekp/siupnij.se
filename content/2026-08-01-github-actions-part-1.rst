Dzidzi pierwsze kroki w GitHub Actions
######################################

:date: 2026-08-01
:modified: 2026-08-01
:category: programowanie
:slug: github-actions-part-1
:authors: Piotr Kierzek

Uważny czytelnik zapewne zauważy, że zawodowo jestem nominalnie DevOpsem, jednak prawda jest taka, że większość mojej pracy to skupia się bardziej na Operations niż na Development, w dodatku `lwia część Operations jest manualna <https://www.reddit.com/r/devops/comments/y14d3z/is_devops_really_fancy_name_for_sysadmin_in_many/>`_. Jakby tego było mało, nie jestem zaznajomiony w ogóle z ekosystemem GitHub, całą swoją profesjonalną przygodę spędzając na rozwiązaniach bazujących na GitLab. Stąd stwierdziłem, że próba automatycznego aktualizowania strony przy każdej większej zmianie na repozytorium to będzie fajna nowość i możliwość samodoskonalenia umiejętności automatyzacji procesów.

Na początek plan w formie diagramu - bo diagramy są FAJNE:

.. figure:: {static}/images/github_1_flowchart.png
   :alt: Diagram przedstawiający przebieg planowanego procesu automatycznej aktualizacji strony
   :align: center

   ⠀

Poza tym, co widoczne na powyższym diagramatycznym podejściu, fajnie by było, gdyby:
- Przesyłanie odbywało się przyrostowo (żeby ograniczyć zmarnowany przesył danych i nie robić nawet małych problemów z bandwidth dla kochanych Neocities);
- Usunięte zasoby po stronie źródła również były automatycznie usuwane na stronie "produkcyjnej";
- Cały proces sprzątał po sobie i nie zostawiał trwałego śmietnika gdzieś na serwerach GitHub czy tym bardziej w moim repozytorium.

Pierwsza implementacja
======================

Naszym celem w tym kroku będzie stworzenie najbardziej łopatologicznego rozwiązania problemu, które spełnia zupełny plan minimum. Rzeczami nice-to-have czy nawet dobrymi praktykami będziemy się martwić później. Przyszły ja też musi mieć coś do roboty. 🤗 Warto też zaznaczyć, ze skoro to ma być rozwojowe zadanie, będę starał się używać jak najmniej kopii 1:1 gotowych rozwiązań - czegoś jednak warto by się po drodze nauczyć, bo i tak na pewno się okaże, że prawdziwymi workflowami byli przyjaciele, których zrobiliśmy po drodze, jak to się mówi.
Przy pomocy oficjalnej dokumentacji GitHub Actions i kilku wyszukań w googlu (oraz odpaleń błędnie skonfigurowanych pipeline'ów) udało mi się skonfigurować prosty workflow budujący zawartość strony:

.. code-block:: yaml
    
    name: Generate static website
    run-name: Create static output to deploy from repository contents
    on:
      push:
        branches:
          - 'main'
    jobs:
      build:
        runs-on: ubuntu-slim
        steps:
            - name: Check out repository code
              uses: actions/checkout@v6
            - run: pip install pelican
            - name: Generate content
              env:
                SITE_URL: ${{vars.SITE_URL}}
              run: pelican content
            - run: ls output/

Dodatkowo, w pliku ``pelicanconf.py`` zrobiłem coś, co powinno być zrobione już dawno, i zwariablizowałem (Czesław Miłosz byłby dumny) jeden z parametrów w pliku:

.. code-block:: python

    import os
    SITEURL = os.environ['SITE_URL']

Z wyjścia ostatniego kroku widzę, że udało się poprawnie zbudować pożądaną strukturę strony wraz z całą zawartością:

.. code-block:: bash

    ► Run ls output/
  
    2026
    about-me
    archives.html
    authors
    authors.html
    categories
    category
    images
    index.html
    tags

W końcu - zweryfikowałem, że nie muszę dodawać żadnych kroków sprzątających po nas. GitHub tworzy workera specjalnie pod ten workflow i na koniec usuwa wszystkie dane tymczasowe i przenosi maszynę wirtualną do `Krainy Cieni <https://www.youtube.com/watch?v=zEytZO4tIYU>`_.
W tym miejscu chciałem przekazać wygenerowaną zawartość strony do następnego workflow, czym samym zauważyłem nieścisłość w swoim zrozumieniu, co tak naprawdę robię tworząc workflow. To nie jest pojedyncza robota, a cały proces wykonywany za jednym zamachem. Wobec tego, nie powinienem próbować zdefiniować nowego workflow, a dodać krok, który przerzuci zawartość na docelowy serwer do workflow, nad którym właśnie pracuję.

W tym celu użyję już gotowej definicji istniejącego już joba. Tak, wiem, wcześniej pisałem, że chciałbym tego uniknąć, ale korzystanie z jobów innych ludzi, kiedy jest taka możliwość to również użyteczna umiejętność; poza tym, do skonfigurowania połączenia z Neocities potrzebne by były różne pod kroki - autoryzacja, tworzenie struktury plików... Po co odkrywać na nowo koło, kiedy `bcomnes <https://github.com/bcomnes/deploy-to-neocities>`_ zrobił już fenomenalną robotę definicją GitHub Action *deploy-to-neocities*. Dodajemy więc do definicji workflow:

.. code-block:: yaml

    name: Generate and upload static website
    run-name: Create static output and upload it to Neocities
    on:
      push:
        branches:
        - 'main'
    jobs:
      build:
        runs-on: ubuntu-slim
        steps:
          - name: Check out repository code
            uses: actions/checkout@v6
          - run: pip install pelican
          - name: Generate content
            env:
              SITE_URL: ${{vars.SITE_URL}}
            run: pelican content
          - name: Deploy to neocities
            uses: bcomnes/deploy-to-neocities@v3
            with:
              api_key: ${{ secrets.NEOCITIES_API_TOKEN }}
              cleanup: true
              neocities_supporter: true
              preview_before_deploy: true
              dist_dir: output

Sprawdźmy co się stanie, gdy job przejdzie (oszczędzę raportowania kilku nieudanych prób związanych z błędnym syntaksem...)

.. figure:: {static}/images/github_1_strona_bez_css.png
   :alt: Zaktualizowana strona główna pozbawiona stylowania CSS
   :align: center
   :target: {static}/images/github_1_strona_bez_css.png
   :width: 400px

   (kliknij, aby zobaczyć pełny rozmiar)

Co do licha się stało z moim formatowaniem?! Cóż, jako, że dokonałem trochę bardziej daleko idących zmian do motywu `Eevee <https://github.com/kura/eevee>`_, postanowiłem, że będę go trzymał w submodule w `oddzielnym repozytorium <https://github.com/kierzekp/eevee-siupnij.se-flavored>`_. Wszystko super, ale okazuje się, że domyślna definicja joba *actions/checkout* nie będzie też robiła checkoutu submodułów; naprawimy to w prosty sposób...

.. code-block:: yaml

    - name: Check out repository code
      uses: actions/checkout@v6
      with:
        submodules: 'true'

Ta niewielka zmiana sprawiła, że et voila, strona wyświetla się wspaniale! Oprócz małego szczegółu... Zniknęła `Lilijka <https://en.touhouwiki.net/wiki/Lily_White>`_!

.. figure:: {static}/images/github_1_zaginela_lily.png
   :alt: Zbliżenie na fragment strony głównej, w którym powinna być pikselowa grafika Lily White.
   :align: center
   :target: {static}/images/github_1_zaginela_lily.png
   :width: 400px

   (kliknij, aby zobaczyć pełny rozmiar)

Po krótkim dochodzeniu udało mi się dojść, co jest nie tak. Problematyczne okazały się, a jakżę, relatywne ścieżki do plików zawartych w motywie. Szybki szacher-macher w bazowym HTML dla motywu i już wszytsko działa jak powinno. Dodatkowo, postanowiłem zamienić (absolutnie wspaniałą) grafikę autorstwa `Suwa Lagito <https://danbooru.donmai.us/posts/7531565>`_ na przerobioną na odpowiednie kolorki sówkę, gdyż jest to jednak znak rozpoznawalny siupania.

.. figure:: {static}/images/github_1_koniec.png
   :alt: Efekt końcowy prac
   :align: center
   :target: {static}/images/github_1_koniec.png
   :width: 400px

   (kliknij, aby zobaczyć pełny rozmiar)

Następnym razem być może spróbujemy zrobić własną implementację akcji *deploy-to-neocities*. Póki co, cieszę się z aktualnego poziomu automatyzacji i cieszę się, że mogłem nauczyć się czegoś nowego.