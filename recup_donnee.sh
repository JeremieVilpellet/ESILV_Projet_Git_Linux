page=$(curl https://www.abcbourse.com/download/valeur/KOu)
tableau_hist=$(echo "$page" | grep -ozP '<table((?!<table).|\n|\t)*?Date(.|\n|\t)*?</table')
tableau_colonnes=$(echo "$tableau_hist" | grep -oP '<th.*?>\K.*?(?=</th>)')
colonnes=0
IFS="
"
for colonne in $tableau_colonnes; do
    colonnes=$((colonnes+1))
done
echo "" > donnee_historique.csv
i=0
for colonne in $tableau_colonnes; do
    i=$((i+1))
    if [ $((i%colonnes)) -eq 0 ]; then
        echo "$colonne" >> donnee_historique.csv
    else
        echo -n "$colonne;" >> donnee_historique.csv
    fi
done

tableau_lignes=$(echo "$tableau_hist" | grep -oP '<td.*?>\K.*?(?=</td>)'| sed 's/&#xA0;//g' | sed 's/<span.*>\(.*\)<\/span>/\1/g' | sed 's/,/./g')
i=0
for ligne in $tableau_lignes; do
    i=$((i+1))
    if [ $((i%colonnes)) -eq 0 ]; then
        echo "$ligne" >> donnee_historique.csv
    else
        echo -n "$ligne;" >> donnee_historique.csv
    fi
done

