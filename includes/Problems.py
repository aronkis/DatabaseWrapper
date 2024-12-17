problema3_a = "SELECT * \
               FROM Deviz \
               WHERE data_constatare IS NOT NULL \
               AND (data_finalizare IS NULL OR data_finalizare > DATE '2024-03-01') \
               ORDER BY data_constatare DESC, data_introducere ASC;"
           
problema3_b = "Select * \
               FROM Piesa \
               WHERE pret_c > 10 \
               ORDER BY pret_c ASC;"

problema4_a = "SELECT \
               p.id, \
               p.nume AS nume_depanator, \
               pi.descriere, \
               pi.fabricant, \
               pi.pret_c, \
               pd.pret_r \
               FROM Piesa_Deviz pd \
               JOIN Piesa pi ON pd.id_p = pi.id_p \
               JOIN Deviz d ON pd.id_d = d.id_d \
               JOIN Persoana p ON d.id_depanator = p.id \
               WHERE pi.pret_c > pd.pret_r;" 

problema4_b = "SELECT DISTINCT \
               pd1.id_d AS id_d1, \
               pd2.id_d AS id_d2 \
               FROM Piesa_Deviz pd1 \
               JOIN Piesa_Deviz pd2  \
               ON pd1.id_p = pd2.id_p  \
               AND pd1.cantitate = pd2.cantitate \
               WHERE pd1.id_d < pd2.id_d;"

problema5_a = "SELECT \
               d.* \
               FROM Deviz d \
               JOIN Piesa_Deviz pd ON pd.id_d = d.id_d \
               JOIN Piesa p ON pd.id_p = p.id_p \
               WHERE LOWER(p.descriere) LIKE '%surub%' \
               ORDER BY pd.cantitate ASC \
               LIMIT 1;" 

problema5_b = "SELECT  \
               p.id_p, \
               p.descriere, \
               p.fabricant \
               FROM  \
               Piesa p \
               WHERE  \
               p.pret_c IN ( \
                   SELECT pd.pret_r \
                   FROM Piesa_Deviz pd \
                   WHERE pd.id_d = 1 AND pd.id_p = 1 \
               )"

problema6_a = "SELECT \
               d.id_depanator, \
               MIN(d.total) AS min_total, \
               AVG(d.total) AS avg_total, \
               MAX(d.total) AS max_total \
               FROM \
               Deviz d \
               WHERE \
               EXTRACT(YEAR FROM d.data_introducere) = 2024 \
               GROUP BY \
               d.id_depanator;" 

problema6_b = "SELECT \
               d.id_d, \
               pd.cantitate * pd.pret_r AS Valoarea_Reala \
               FROM \
               Deviz d \
               JOIN \
               Piesa_Deviz pd ON d.id_d = pd.id_d \
               ORDER BY \
               d.id_d;"
