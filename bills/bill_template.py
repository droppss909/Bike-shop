html_template = """
<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Faktura VAT</title>
<style>
    body {{
        font-family: Arial, sans-serif;
    }}
    .container {{
        width: 80%;
        margin: 0 auto;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }}
    th, td {{
        border: 1px solid #000;
        padding: 8px;
        text-align: left;
    }}
    th {{
        background-color: #f2f2f2;
    }}
    .total {{
        font-weight: bold;
    }}
</style>
</head>
<body>
<div class="container">
    <h2>Faktura VAT</h2>
    <table>
        <thead>
            <tr>
                <th>Lp.</th>
                <th>Nazwa produktu/usługi</th>
                <th>Ilość</th>
                <th>Cena(PLN)</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
    <div class="total">Suma: {total_price} PLN</div>
    <div>
        <p>Sprzedawca: Skelp rowerowy sp. Z.O.O</p>
        <p>Nazwa firmy</p>
        <p>Adres</p>
        <p>NIP: 12345678</p>
    </div>
    <div>
        <p>Nabywca:</p>
        <p>Imię i nazwisko / Nazwa firmy: {buyer}</p>
        <p>NIP: {buyer_nip}</p>
    </div>
</div>
</body>
</html>
"""