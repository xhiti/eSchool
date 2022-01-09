from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('lendet/', views.lendet, name='subjects'),
    path('lendet/shto/', views.shto_lende, name='add-subject'),
    path('lendet/fshi/<str:code>/', views.fshi_lende, name='delete-subject'),
    path('lendet/modifiko/<str:code>/', views.modifiko_lende, name='edit-subject'),

    path('nxenesit/', views.nxenesit, name='students'),
    path('nxenesit/shto/', views.shto_nxenes, name='add-student'),
    path('nxenesit/fshi/<str:code>/', views.fshi_nxenes, name='delete-student'),
    path('nxenesit/info/<str:code>/', views.info_nxenes, name='info-student'),
    path('nxenesit/modifiko/<str:code>/', views.modifiko_nxenes, name='edit-student'),
    path('nxenesit/printo/<str:code>/', views.printo_nxenes, name='print-student'),

    path('prinderit/', views.prinderit, name='parents'),
    path('prinderit/shto/', views.shto_prind, name='add-parent'),
    path('prinderit/fshi/<str:code>/', views.fshi_prind, name='delete-parent'),
    path('prinderit/modifiko/<str:code>/', views.modifiko_prind, name='edit-parent'),

    path('statistika/', views.statistika, name='statistics'),
    path('nota/shto/', views.shto_note, name='add-grade'),

    path('klasa-8-a/nxenesit/', views.klasa_8_a, name='class-8-a'),
    path('klasa-8-a/nxenesit/shto/', views.klasa_8_a_shto_nxenes, name='add-student-8-a'),
    path('klasa-8-a/nota/shto/', views.klasa_8_a_shto_note, name='add-grade-8-a'),

    path('klasa-8-d/nxenesit/', views.klasa_8_d, name='class-8-d'),
    path('klasa-8-d/nxenesit/shto/', views.klasa_8_d_shto_nxenes, name='add-student-8-d'),
    path('klasa-8-d/nota/shto/', views.klasa_8_d_shto_note, name='add-grade-8-d'),

    path('klasa-8-e/nxenesit/', views.klasa_8_e, name='class-8-e'),
    path('klasa-8-e/nxenesit/shto/', views.klasa_8_e_shto_nxenes, name='add-student-8-e'),
    path('klasa-8-e/nota/shto/', views.klasa_8_e_shto_note, name='add-grade-8-e'),

    path('klasa-9-e/nxenesit/', views.klasa_9_e, name='class-9-e'),
    path('klasa-9-e/nxenesit/shto/', views.klasa_9_e_shto_nxenes, name='add-student-9-e'),
    path('klasa-9-e/nota/shto/', views.klasa_9_e_shto_note, name='add-grade-9-e'),

    path('klasa-kujdestari/lista-e-detyrimit/', views.printo_liste_detyrimi, name='printo-liste-detyrimi'),
    path('klasa-kujdestari/lista-e-prinderve/', views.printo_liste_prinderish, name='printo-liste-prinderish'),

    path('klasa-kujdestari/statistika/vjetore/', views.printo_statistike_vjetore_klasa_kujdestari, name='printo-statistika-vjetore'),
    path('klasa-kujdestari/statistika/periudha-1/', views.printo_statistike_periudha_1_klasa_kujdestari, name='printo-statistika-periudha-1'),
    path('klasa-kujdestari/statistika/periudha-2/', views.printo_statistike_periudha_2_klasa_kujdestari, name='printo-statistika-periudha-2'),
    path('klasa-kujdestari/statistika/periudha-3/', views.printo_statistike_periudha_3_klasa_kujdestari, name='printo-statistika-periudha-3'),

    path('klasa-8-a/statistika/vjetore/', views.printo_statistike_vjetore_8A, name='printo-statistika-vjetore-klasa-8-a'),
    path('klasa-8-a/statistika/periudha-1/', views.printo_statistike_periudha_1_8A, name='printo-statistika-periudha-1-klasa-8-a'),
    path('klasa-8-a/statistika/periudha-2/', views.printo_statistike_periudha_2_8A, name='printo-statistika-periudha-2-klasa-8-a'),
    path('klasa-8-a/statistika/periudha-3/', views.printo_statistike_periudha_3_8A, name='printo-statistika-periudha-3-klasa-8-a'),

    path('klasa-8-d/statistika/vjetore/', views.printo_statistike_vjetore_8D, name='printo-statistika-vjetore-klasa-8-d'),
    path('klasa-8-d/statistika/periudha-1/', views.printo_statistike_periudha_1_8D, name='printo-statistika-periudha-1-klasa-8-d'),
    path('klasa-8-d/statistika/periudha-2/', views.printo_statistike_periudha_2_8D, name='printo-statistika-periudha-2-klasa-8-d'),
    path('klasa-8-d/statistika/periudha-3/', views.printo_statistike_periudha_3_8D, name='printo-statistika-periudha-3-klasa-8-d'),

    path('klasa-8-e/statistika/vjetore/', views.printo_statistike_vjetore_8E, name='printo-statistika-vjetore-klasa-8-e'),
    path('klasa-8-e/statistika/periudha-1/', views.printo_statistike_periudha_1_8E, name='printo-statistika-periudha-1-klasa-8-e'),
    path('klasa-8-e/statistika/periudha-2/', views.printo_statistike_periudha_2_8E, name='printo-statistika-periudha-2-klasa-8-e'),
    path('klasa-8-e/statistika/periudha-3/', views.printo_statistike_periudha_3_8E, name='printo-statistika-periudha-3-klasa-8-e'),

    path('klasa-9-e/statistika/vjetore/', views.printo_statistike_vjetore_9E, name='printo-statistika-vjetore-klasa-9-e'),
    path('klasa-9-e/statistika/periudha-1/', views.printo_statistike_periudha_1_9E, name='printo-statistika-periudha-1-klasa-9-e'),
    path('klasa-9-e/statistika/periudha-2/', views.printo_statistike_periudha_2_9E, name='printo-statistika-periudha-2-klasa-9-e'),
    path('klasa-9-e/statistika/periudha-3/', views.printo_statistike_periudha_3_9E, name='printo-statistika-periudha-3-klasa-9-e'),

]
