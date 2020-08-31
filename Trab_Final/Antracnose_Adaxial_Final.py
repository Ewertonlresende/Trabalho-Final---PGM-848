
# USO DE ANÁLISE DE IMAGENS NA AVALIAÇÃO DE SINTOMAS DE ANTRACNOSE NO FEIJOEIRO
########################################################################################################################
# DATA: 31/08/2020
# DISCIPLINA: VISÃO COMPUTACIONAL NO MELHORAMENTO DE PLANTAS
# PROFESSOR: VINÍCIUS QUINTÃO CARNEIRO
# ALUNOS:
# CAROLINE MARCELA DA SILVA
# EWERTON LÉLYS RESENDE
# MARIANA ANDRADE DIAS
# THIAGO TAVARES BOTELHO
########################################################################################################################

#Importar pacotes
import cv2 # Importa o pacote opencv
import os
import glob
import pandas as pd

os.chdir(r'C:\Users\Usuario\Desktop\PycharmProjects\Ewerton\REO 02\LISTA_3')
# Diretório das imagens
path_of_images=r'C:\Users\Usuario\Desktop\PycharmProjects\Ewerton\REO 02\LISTA_3\Trab_Final\folha adaxial'
mask_folhas =r'C:\Users\Usuario\Desktop\PycharmProjects\Ewerton\REO 02\LISTA_3\Trab_Final\folha adaxial\seg'
mask_lesoes =r'C:\Users\Usuario\Desktop\PycharmProjects\Ewerton\REO 02\LISTA_3\Trab_Final\folha adaxial\antracnose'

filenames= glob.glob(path_of_images + "/*.jpg")
dimen = []
i=1

for imagem in filenames:
    img = cv2.imread(imagem)
    img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    b = img_rgb[:,:,2]
    img_filtro_mediana1 = cv2.medianBlur(b, 21)
    _ , img_limiar = cv2.threshold(img_filtro_mediana1,100,255,cv2.THRESH_BINARY_INV)
    img_segmentada1 = cv2.bitwise_and(img_rgb,img_rgb,mask=img_limiar)

    nome_legenda = os.path.basename(imagem)
    (x, y, w, h) = cv2.boundingRect(img_limiar)
    obj_rgb = img_segmentada1[y:y+h,x:x+w]
    obj_bgr = cv2.cvtColor(obj_rgb,cv2.COLOR_RGB2BGR)
    cv2.imwrite(os.path.join(mask_folhas, nome_legenda), obj_bgr)

    area = cv2.countNonZero(img_limiar)
    det = nome_legenda[7:9]

    if det == 'ab':
        # Seguimentação folhas Abaxial
        hsv = cv2.cvtColor(obj_bgr, cv2.COLOR_BGR2HSV)
        s = hsv[:, :, 1]
        _, thrsh1 = cv2.threshold(s, 200, 255, cv2.THRESH_BINARY)
        area_lesao = cv2.countNonZero(thrsh1)
        img_segmentada2 = cv2.bitwise_and(obj_bgr, obj_bgr, mask=thrsh1)
        cv2.imwrite(os.path.join(mask_lesoes, nome_legenda), thrsh1)

        por_in = ((area_lesao) / (area) * 100).__round__(2)
    else:
        # Área lesão adaxial
        hsv= cv2.cvtColor(img_rgb,cv2.COLOR_RGB2HSV)
        h = hsv[:, :, 0]
        _,thrsh1 = cv2.threshold(h, 70, 255, cv2.THRESH_BINARY_INV)
        area_lesao = cv2.countNonZero(thrsh1)
        por_in = (((area - area_lesao)/area)*100).__round__(2)
        cv2.imwrite(os.path.join(mask_lesoes, nome_legenda), thrsh1)

    legenda = nome_legenda[:-4]

    dimen += [[str(legenda),str(area_lesao),str(area),str(por_in)]]

    a = i / (len(filenames)) * 100
    print("{0:.2f} % completed".format(round(a, 2)))
    i = i + 1

dados_folhas = pd.DataFrame(dimen)
dados_folhas = dados_folhas.rename(columns={0: 'Imagem', 1: 'Area_da_lesao',
                                            2:'Area_folha',3:'Porcentagem_infectado' })
dados_folhas.to_csv('medida_ad.csv', index=False)







