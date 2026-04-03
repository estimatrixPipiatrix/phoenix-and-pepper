Phoenix et Piper — Ars Interrogandi (SQL)

Haec documenta artem SQL per exempla docent. Omnia exempla contra basim datorum Phoenix et Piper currunt.

Fundamenta

SQL sententias continet quae semper eodem ordine scribuntur:

SELECT — quid spectare velis
FROM — ex qua tabula petas
WHERE — quos ordines eligas
GROUP BY — quomodo ordines in classes digeras
ORDER BY — quo ordine disponas
LIMIT — quot ordines accipias

Non omnes partes semper necessariae sunt; ordo tamen idem manet. Sententia puncto atque virgula (;) terminatur.

SELECT et FROM

Haec est omnium interrogationum basis: quid spectare velis et unde?

Omnia ex tabula:

SELECT * FROM ports;

Asteriscus (*) omnes columnas significat. Exitus: omnes portus cum omnibus attributis.

Columnas nominatas:

SELECT name, size FROM ports;

Tantum nomen et magnitudinem portuum ostendit.

WHERE

WHERE ordines eligit: hos tantum volo.

Aequalitas:

SELECT name, size FROM ports WHERE size = 5;

Exitus: Ostia et Puteoli (soli portus huius magnitudinis).

Comparationes:

SELECT name, base_fee FROM ports WHERE base_fee > 35;

Operatores: = (aequale), > (maius), < (minus), ≥ (maius vel aequale), ≤ (minus vel aequale), ≠ (inaequale).

Plures condiciones:

SELECT name, size, base_fee FROM ports
WHERE size >= 4 AND base_fee > 40;

AND significat utrumque verum esse; OR significat alterutrum verum esse.

SELECT name, danger_type FROM routes
WHERE danger_type = 'mythological'
   OR danger_type = 'divine';

Textus cum IN:

SELECT name, customer_type FROM customers
WHERE customer_type IN ('mercator', 'magus');

IN significat in hac serie contineri; brevius est quam multas condiciones OR scribere.

Textus cum LIKE:

SELECT name FROM ships WHERE name LIKE 'F%';

% significat quidlibet post hoc. Exitus: Fortuna Lenta.

Valores nulli:

SELECT name, special_handling FROM cargo_types
WHERE special_handling IS NULL;

NULL peculiari ratione tractatur — non = NULL, sed IS NULL scribimus.

SELECT name, special_handling FROM cargo_types
WHERE special_handling IS NOT NULL;

ORDER BY

ORDER BY ordines disponit: hoc ordine ostende.

A minimo ad maximum:

SELECT name, base_fee FROM ports ORDER BY base_fee;

Panormus (25) primus, Puteoli (55) ultimus.

A maximo ad minimum:

SELECT name, base_fee FROM ports ORDER BY base_fee DESC;

DESC significat descendentem ordinem.

Pluribus columnis:

SELECT name, cargo_class, unit_price_denarii
FROM cargo_types
ORDER BY cargo_class, unit_price_denarii DESC;

Primum per classem, deinde intra eandem classem per pretium.

LIMIT

LIMIT numerum ordinum restringit: tantum primos N accipe.

SELECT name, unit_price_denarii
FROM cargo_types
ORDER BY unit_price_denarii DESC
LIMIT 3;

Tres merces pretiosissimas ostendit.

COUNT, SUM, AVG, MIN, MAX

Functiones aggregationis: de multis ordinibus aliquid computa.

Numerare:

SELECT COUNT(*) FROM customers;

Quot clientes habemus?

Summam:

SELECT SUM(quantity) FROM order_lines;

Quantitas universa omnium ordinum.

Medium:

SELECT AVG(base_fee) FROM ports;

Vectigal medium portuum.

Minimum et maximum:

SELECT MIN(unit_price_denarii), MAX(unit_price_denarii)
FROM cargo_types;

Pretium vilissimum et carissimum.

GROUP BY

GROUP BY ordines in classes digerit, deinde aggregationem per singulas classes facit.

Numerare per classes:

SELECT customer_type, COUNT(*)
FROM customers
GROUP BY customer_type;

Quot clientes cuiusque generis sunt?

Summam per classes:

SELECT cargo_class, SUM(ol.quantity) AS total_quantity
FROM order_lines ol
JOIN cargo_types c ON ol.cargo_type_id = c.id
GROUP BY cargo_class;
HAVING

HAVING est quasi WHERE post GROUP BY:

SELECT cargo_class, SUM(ol.quantity) AS total_quantity
FROM order_lines ol
JOIN cargo_types c ON ol.cargo_type_id = c.id
GROUP BY cargo_class
HAVING SUM(ol.quantity) > 100;
AS (Cognomina)

AS columnis nomina clariora vel breviora dat:

SELECT name AS portus, base_fee AS vectigal FROM ports;

AS basim datorum non mutat, sed solum nomen in exitu.

SELECT COUNT(*) AS numerus_clientium FROM customers;
JOIN

JOIN tabulas coniungit—hoc est cor SQL.

JOIN simplex:

SELECT s.name, st.name AS ship_type
FROM ships s
JOIN ship_types st ON s.ship_type_id = st.id;

“Da mihi nomen navis et generis eius.”
Duae tabulae coniunguntur ubi columnae inter se respondent.

Litterae s et st sunt cognomina tabularum.

Plures JOIN:

SELECT s.name AS navis,
       st.name AS genus,
       p.name AS portus_domesticus
FROM ships s
JOIN ship_types st ON s.ship_type_id = st.id
JOIN ports p ON s.home_port_id = p.id;

JOIN cum WHERE:

SELECT s.name, st.name AS ship_type
FROM ships s
JOIN ship_types st ON s.ship_type_id = st.id
WHERE st.can_carry_phoenix = true;

JOIN cum GROUP BY:

SELECT c.name AS merx,
       c.cargo_class,
       SUM(ol.quantity) AS total_ordered
FROM order_lines ol
JOIN cargo_types c ON ol.cargo_type_id = c.id
GROUP BY c.name, c.cargo_class
ORDER BY total_ordered DESC;

Catena longa:

SELECT cu.name AS cliens,
       c.name AS merx,
       ol.quantity
FROM orders o
JOIN customers cu ON o.customer_id = cu.id
JOIN order_lines ol ON ol.order_id = o.id
JOIN cargo_types c ON ol.cargo_type_id = c.id
WHERE cu.name = 'Decimus Obscurus';
Pecunia (arithmetica in SELECT)
SELECT c.name,
       ol.quantity,
       c.unit_price_denarii,
       ol.quantity * c.unit_price_denarii AS reditus
FROM order_lines ol
JOIN cargo_types c ON ol.cargo_type_id = c.id
ORDER BY reditus DESC;

Reditus per classem:

SELECT c.cargo_class,
       SUM(ol.quantity * c.unit_price_denarii) AS total_reditus
FROM order_lines ol
JOIN cargo_types c ON ol.cargo_type_id = c.id
GROUP BY c.cargo_class;

Per clientem:

SELECT cu.name,
       cu.customer_type,
       SUM(ol.quantity * c.unit_price_denarii) AS summa_impensa
FROM orders o
JOIN customers cu ON o.customer_id = cu.id
JOIN order_lines ol ON ol.order_id = o.id
JOIN cargo_types c ON ol.cargo_type_id = c.id
GROUP BY cu.name, cu.customer_type
ORDER BY summa_impensa DESC;
Interrogationes utiles

Quot itinera mythologica sunt?

SELECT COUNT(*) AS itinera_mythologica
FROM routes
WHERE danger_type = 'mythological';

Quae navis quot navigationes fecit?

SELECT s.name, COUNT(*) AS navigationes
FROM voyages v
JOIN ships s ON v.ship_id = s.id
GROUP BY s.name
ORDER BY navigationes DESC;

Quae itinera periculosissima sunt?

SELECT p1.name AS origo,
       p2.name AS destinatio,
       r.danger_level,
       r.danger_type
FROM routes r
JOIN ports p1 ON r.origin_port_id = p1.id
JOIN ports p2 ON r.destination_port_id = p2.id
WHERE r.danger_level >= 3
ORDER BY r.danger_level DESC;

Quid in nave nunc est?

SELECT s.name AS navis,
       c.name AS merx,
       ol.quantity
FROM voyages v

JOIN voyage_manifest vm ON vm.voyage_id = v.id
JOIN order_lines ol ON vm.order_line_id = ol.id
JOIN cargo_types c ON ol.cargo_type_id = c.id
WHERE v.status = 'in_transit';
Summa

Ordo verborum SQL:

SELECT — quid spectes
FROM — unde incipias
JOIN — alias tabulas conectas
WHERE — ordines eligas
GROUP BY — in classes digeras
HAVING — classes eligas
ORDER BY — ordines disponas
LIMIT — numerum finias

Haec omnia coniuncta quaestionibus negotii respondent.
