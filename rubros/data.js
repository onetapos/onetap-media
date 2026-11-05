const G = s => `<span class="gold">${s}</span>`;
const card = (n, s, v, cls='') => `<div class="card ai ${cls}"><div><b>${n}</b>${s?`<span class="s">${s}</span>`:''}</div>${v?`<div class="v">${v}</div>`:''}</div>`;
const note = (cls, txt) => `<div class="note ai ${cls}">${txt}</div>`;
const DATA = {
 clin: {
  es: {
   big1: ['Agenda','llena','no','siempre','es','agenda',G('ordenada.')],
   hook: ['¿Cuántas','citas','se','te','pierden','al',G('mes?')],
   big2: ['Confirmar','cita','por','cita','te','roba','la',G('tarde.')],
   tags: [['Lunes 10:00','Cita doble',520,640],['Martes 11:30','No vino',60,820],['Jueves 3:00 p. m.','Hueco',470,1010],['Viernes 9:00','Canceló tarde',60,1190]],
   cost: ['Citas perdidas este mes','8','Valor por cita','$45.00','Dejaste de cobrar','$360'],
   illus: 'Ejemplo ilustrativo',
   uiK: 'ONETAP · AGENDA', uiT: 'Tu agenda en orden,<br>sin cruces.',
   screens: [
    {h:'Agenda de hoy', s:'Por profesional', html:`<div class="chips ai"><span class="chip on">Dra. Pérez</span><span class="chip">Dr. Castillo</span></div>`+card('8:00 · Limpieza','Ana M.','')+card('9:00 · Control','Luis R.','')+card('10:30 · Blanqueamiento','Sofía G.','')+card('12:00 · Ortodoncia','Marco T.','')+card('3:00 p. m. · Disponible','','', 'free')},
    {h:'Nueva cita', s:'Sin cruces', html: card('Profesional','Dra. Pérez','')+card('Hora','Martes 10:30','')+note('warn','Horario ocupado: 10:30 ya tiene cita')+note('ok','Disponible: 11:00')+`<div class="btnx ai">Agendar 11:00</div>`},
    {h:'Recordatorio', s:'WhatsApp · sin costo por mensaje', html:`<div class="wa"><div class="hdr ai">WhatsApp · Ana M.</div><div class="bub out ai">Hola Ana, te recordamos tu cita mañana a las 11:00 con la Dra. Pérez.<small>7:00 p. m. ✓✓</small></div><div class="bub in ai">¡Perfecto, ahí estaré!<small>7:04 p. m.</small></div></div>`+note('gold','Enviado automáticamente')},
    {h:'Recordatorios de mañana', s:'Enviados por WhatsApp', dark:true, html: card('Ana M.','11:00 · Dra. Pérez','<span class="ok">✓</span>')+card('Luis R.','9:00 · Dr. Castillo','<span class="ok">✓</span>')+card('Sofía G.','10:30 · Dra. Pérez','<span class="ok">✓</span>')+card('Marco T.','12:00 · Dr. Castillo','<span class="ok">✓</span>')+card('Enviados hoy','',`<span data-to="14">0</span>`)},
   ],
   fc: [['Por profesional','Cada uno su agenda'],['Sin cruces','Te avisa al instante'],['WhatsApp','Sin costo por mensaje'],['Automático','Todos los días']],
   brief: {t:'Tu día de hoy', s:'7:00 a. m. · 3 acciones', a:['14 citas hoy y un hueco a las 3:00 p. m.','El martes viene lleno: abre más horarios','6 pacientes no vuelven hace 3 meses: escríbeles']},
   end: {l1:'Tu agenda en orden.<br>Sin cruces.', btn:'Primer mes gratis', sub:'Sin tarjeta · onetaphq.com'},
  },
  en: {
   big1: ['A','full','schedule','isn\'t','always','an',G('organized'),'one.'],
   hook: ['How','many','appointments','slip','away','every',G('month?')], hookSize: 112,
   big2: ['Confirming','one','by','one','steals','your',G('afternoon.')],
   tags: [['Mon 10:00','Double-booked',520,640],['Tue 11:30','No-show',60,820],['Thu 3:00 p.m.','Empty slot',470,1010],['Fri 9:00','Late cancel',60,1190]],
   cost: ['Missed visits this month','8','Value per visit','$45.00','Revenue lost','$360'],
   illus: 'Illustrative example',
   uiK: 'ONETAP · SCHEDULING', uiT: 'Your schedule in order,<br>zero overlaps.',
   screens: [
    {h:'Today\'s schedule', s:'By professional', html:`<div class="chips ai"><span class="chip on">Dr. Perez</span><span class="chip">Dr. Castillo</span></div>`+card('8:00 · Cleaning','Ana M.','')+card('9:00 · Check-up','Luis R.','')+card('10:30 · Whitening','Sofia G.','')+card('12:00 · Braces','Marco T.','')+card('3:00 p.m. · Open','','','free')},
    {h:'New appointment', s:'Zero overlaps', html: card('Professional','Dr. Perez','')+card('Time','Tuesday 10:30','')+note('warn','Slot taken: 10:30 is already booked')+note('ok','Available: 11:00')+`<div class="btnx ai">Book 11:00</div>`},
    {h:'Reminder', s:'WhatsApp · no cost per message', html:`<div class="wa"><div class="hdr ai">WhatsApp · Ana M.</div><div class="bub out ai">Hi Ana, a quick reminder of your appointment tomorrow at 11:00 with Dr. Perez.<small>7:00 p.m. ✓✓</small></div><div class="bub in ai">Perfect, see you there!<small>7:04 p.m.</small></div></div>`+note('gold','Sent automatically')},
    {h:'Tomorrow\'s reminders', s:'Sent on WhatsApp', dark:true, html: card('Ana M.','11:00 · Dr. Perez','<span class="ok">✓</span>')+card('Luis R.','9:00 · Dr. Castillo','<span class="ok">✓</span>')+card('Sofia G.','10:30 · Dr. Perez','<span class="ok">✓</span>')+card('Marco T.','12:00 · Dr. Castillo','<span class="ok">✓</span>')+card('Sent today','',`<span data-to="14">0</span>`)},
   ],
   fc: [['By professional','Each one, their own'],['Zero overlaps','Flags conflicts'],['WhatsApp','No cost per message'],['Automatic','Every single day']],
   brief: {t:'Today\'s briefing', s:'7:00 a.m. · 3 actions', a:['14 appointments today, one open slot at 3:00 p.m.','Tuesday is full: open more slots','6 patients haven\'t returned in 3 months: reach out']},
   end: {l1:'Your schedule in order.<br>Zero overlaps.', btn:'First month free', sub:'No card required · onetaphq.com'},
  }
 },
 manu: {
  es: {
   big1: ['Producción','a','tope','no','siempre','es','producción',G('rentable.')],
   hook: ['¿Cuánto','material','se','te','va','sin','que','lo',G('sepas?')], hookSize: 108,
   big2: ['El','conteo','a','mano','te','roba','la',G('noche.')],
   tags: [['Harina 50 kg','$38.00',540,720],['Azúcar 25 kg','$21.50',60,880],['Mantequilla 10 kg','$64.00',470,1050],['Empaques 500 u','$30.00',60,1210]],
   cost: ['Compraste este mes','$4,850','Merma sin registrar','6%','Se te fue','$291'],
   illus: 'Ejemplo ilustrativo',
   uiK: 'ONETAP · PRODUCCIÓN', uiT: 'Del insumo al producto,<br>sin perder la cuenta.',
   screens: [
    {h:'Lista de materiales', s:'Galletas de avena · 200 u', html: card('Harina','12 kg','$9.12')+card('Avena','8 kg','$11.20')+card('Azúcar','5 kg','$4.30')+card('Mantequilla','4 kg','$25.60')+card('Empaques','200 u','$12.00')+card('Costo por unidad','',`<span data-to="0.31" data-dec="2" data-pre="$">$0.00</span>`,'tot')},
    {h:'Orden de producción #128', s:'200 galletas · hoy', html: note('ok','Producción registrada')+card('Harina','Descontado del inventario','−12 kg')+card('Avena','Descontado del inventario','−8 kg')+card('Azúcar','Descontado del inventario','−5 kg')+card('Mantequilla','Descontado del inventario','−4 kg')+card('Empaques','Descontado del inventario','−200 u')},
    {h:'Inventario', s:'Lotes y vencimientos', html: card('Harina · Lote H-0921','Bodega 1 · Vence 12 dic','86 kg')+card('Avena · Lote A-0310','Bodega 2','6 kg','hl')+note('warn','Avena bajo el mínimo')+card('Mantequilla · Lote M-0118','Bodega 1 · Vence 18 nov','22 kg')+note('gold','Lote M-0118 vence pronto')},
    {h:'Orden de compra', s:'Según tu consumo', dark:true, html: card('Avena','Proveedor de granos','50 kg')+card('Mantequilla','Proveedor de lácteos','20 kg')+card('Empaques','Proveedor de empaques','1,000 u')+note('ok','Enviada por WhatsApp al proveedor')},
   ],
   fc: [['Lista de materiales','Costo por unidad'],['Producción','Descuenta insumos'],['Lotes','Y vencimientos'],['Compras','Según consumo']],
   brief: {t:'Tu día de hoy', s:'7:00 a. m. · 3 acciones', a:['La avena alcanza para 2 días: pide 50 kg hoy','El lote H-0921 vence en 9 días: úsalo primero','La merma de harina subió 3% esta semana']},
   end: {l1:'Cada insumo, contado.<br>Cada lote, rastreado.', btn:'Primer mes gratis', sub:'Sin tarjeta · onetaphq.com'},
  },
  en: {
   big1: ['A','busy','production','floor','isn\'t','always','a',G('profitable'),'one.'],
   hook: ['How','much','material','slips','away','without','you',G('knowing?')], hookSize: 108,
   big2: ['Counting','by','hand','steals','your',G('nights.')],
   tags: [['Flour 110 lb','$38.00',560,720],['Sugar 55 lb','$21.50',60,880],['Butter 22 lb','$64.00',500,1050],['Packaging 500 u','$30.00',60,1210]],
   cost: ['Purchased this month','$4,850','Unrecorded waste','6%','Money lost','$291'],
   illus: 'Illustrative example',
   uiK: 'ONETAP · PRODUCTION', uiT: 'Raw material to product,<br>every unit counted.',
   screens: [
    {h:'Bill of materials', s:'Oat cookies · 200 u', html: card('Flour','26 lb','$9.12')+card('Oats','18 lb','$11.20')+card('Sugar','11 lb','$4.30')+card('Butter','9 lb','$25.60')+card('Packaging','200 u','$12.00')+card('Cost per unit','',`<span data-to="0.31" data-dec="2" data-pre="$">$0.00</span>`,'tot')},
    {h:'Production order #128', s:'200 cookies · today', html: note('ok','Production recorded')+card('Flour','Deducted from stock','−26 lb')+card('Oats','Deducted from stock','−18 lb')+card('Sugar','Deducted from stock','−11 lb')+card('Butter','Deducted from stock','−9 lb')+card('Packaging','Deducted from stock','−200 u')},
    {h:'Inventory', s:'Lots and expiry dates', html: card('Flour · Lot H-0921','Warehouse 1 · Exp. Dec 12','190 lb')+card('Oats · Lot A-0310','Warehouse 2','13 lb','hl')+note('warn','Oats below minimum')+card('Butter · Lot M-0118','Warehouse 1 · Exp. Nov 18','48 lb')+note('gold','Lot M-0118 expires soon')},
    {h:'Purchase order', s:'Based on your usage', dark:true, html: card('Oats','Grain supplier','110 lb')+card('Butter','Dairy supplier','44 lb')+card('Packaging','Packaging supplier','1,000 u')+note('ok','Sent to supplier on WhatsApp')},
   ],
   fc: [['Bill of materials','Cost per unit'],['Production','Deducts raw materials'],['Lots','And expiry dates'],['Purchasing','Based on usage']],
   brief: {t:'Today\'s briefing', s:'7:00 a.m. · 3 actions', a:['Oats last 2 more days: order 110 lb today','Lot H-0921 expires in 9 days: use it first','Flour waste rose 3% this week']},
   end: {l1:'Every input counted.<br>Every lot traced.', btn:'First month free', sub:'No card required · onetaphq.com'},
  }
 }
};
