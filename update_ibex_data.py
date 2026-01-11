#!/usr/bin/env python3
"""
Script para actualizar datos del IBEX 35 desde Yahoo Finance
Genera un archivo JSON con la información actualizada
"""

import yfinance as yf
import json
from datetime import datetime
import time

# Empresas del IBEX 35 con sus tickers de Yahoo Finance y sectores
IBEX_35_COMPANIES = [
    {'name': 'Inditex', 'ticker': 'ITX.MC', 'sector': 'Consumo'},
    {'name': 'Banco Santander', 'ticker': 'SAN.MC', 'sector': 'Banca'},
    {'name': 'Iberdrola', 'ticker': 'IBE.MC', 'sector': 'Energía'},
    {'name': 'BBVA', 'ticker': 'BBVA.MC', 'sector': 'Banca'},
    {'name': 'Telefónica', 'ticker': 'TEF.MC', 'sector': 'Telecom'},
    {'name': 'Repsol', 'ticker': 'REP.MC', 'sector': 'Energía'},
    {'name': 'CaixaBank', 'ticker': 'CABK.MC', 'sector': 'Banca'},
    {'name': 'Amadeus', 'ticker': 'AMS.MC', 'sector': 'Tecnología'},
    {'name': 'Ferrovial', 'ticker': 'FER.MC', 'sector': 'Construcción'},
    {'name': 'Naturgy', 'ticker': 'NTGY.MC', 'sector': 'Energía'},
    {'name': 'ACS', 'ticker': 'ACS.MC', 'sector': 'Construcción'},
    {'name': 'Endesa', 'ticker': 'ELE.MC', 'sector': 'Energía'},
    {'name': 'Sabadell', 'ticker': 'SAB.MC', 'sector': 'Banca'},
    {'name': 'Cellnex', 'ticker': 'CLNX.MC', 'sector': 'Telecom'},
    {'name': 'IAG', 'ticker': 'IAG.MC', 'sector': 'Transporte'},
    {'name': 'Grifols', 'ticker': 'GRF.MC', 'sector': 'Farmacia'},
    {'name': 'Acciona', 'ticker': 'ANA.MC', 'sector': 'Energía'},
    {'name': 'Bankinter', 'ticker': 'BKT.MC', 'sector': 'Banca'},
    {'name': 'Aena', 'ticker': 'AENA.MC', 'sector': 'Transporte'},
    {'name': 'Red Eléctrica', 'ticker': 'REE.MC', 'sector': 'Energía'},
    {'name': 'Mapfre', 'ticker': 'MAP.MC', 'sector': 'Seguros'},
    {'name': 'Acerinox', 'ticker': 'ACX.MC', 'sector': 'Industrial'},
    {'name': 'Enagás', 'ticker': 'ENG.MC', 'sector': 'Energía'},
    {'name': 'Unicaja', 'ticker': 'UNI.MC', 'sector': 'Banca'},
    {'name': 'Meliá Hotels', 'ticker': 'MEL.MC', 'sector': 'Turismo'},
    {'name': 'Sacyr', 'ticker': 'SCYR.MC', 'sector': 'Construcción'},
    {'name': 'Solaria', 'ticker': 'SLR.MC', 'sector': 'Energía'},
    {'name': 'Fluidra', 'ticker': 'FDR.MC', 'sector': 'Industrial'},
    {'name': 'Rovi', 'ticker': 'ROVI.MC', 'sector': 'Farmacia'},
    {'name': 'PharmaMar', 'ticker': 'PHM.MC', 'sector': 'Farmacia'},
    {'name': 'Indra', 'ticker': 'IDR.MC', 'sector': 'Tecnología'},
    {'name': 'ArcelorMittal', 'ticker': 'MTS.MC', 'sector': 'Industrial'},
    {'name': 'Merlin Properties', 'ticker': 'MRL.MC', 'sector': 'Inmobiliario'},
    {'name': 'Colonial', 'ticker': 'COL.MC', 'sector': 'Inmobiliario'},
    {'name': 'Logista', 'ticker': 'LOG.MC', 'sector': 'Distribución'}
]

def get_stock_data(ticker, retries=3):
    """
    Obtiene datos de una acción desde Yahoo Finance con reintentos
    """
    for attempt in range(retries):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period='5d')
            
            if len(hist) < 2:
                print(f"⚠️  Datos insuficientes para {ticker}")
                return None
            
            current_price = hist['Close'].iloc[-1]
            previous_price = hist['Close'].iloc[-2]
            change_percent = ((current_price - previous_price) / previous_price) * 100
            
            # Capitalización de mercado en millones
            market_cap = info.get('marketCap', 0) / 1_000_000
            
            return {
                'price': round(current_price, 2),
                'change': round(change_percent, 2),
                'marketCap': round(market_cap, 0)
            }
            
        except Exception as e:
            if attempt < retries - 1:
                print(f"⚠️  Error en {ticker}, reintentando... ({attempt + 1}/{retries})")
                time.sleep(2)
            else:
                print(f"❌ Error obteniendo datos de {ticker}: {str(e)}")
                return None
    
    return None

def get_ibex_index():
    """
    Obtiene datos del índice IBEX 35
    """
    try:
        ibex = yf.Ticker('^IBEX')
        hist = ibex.history(period='5d')
        
        if len(hist) < 2:
            return None
        
        current_value = hist['Close'].iloc[-1]
        previous_value = hist['Close'].iloc[-2]
        change = current_value - previous_value
        change_percent = (change / previous_value) * 100
        
        return {
            'value': round(current_value, 2),
            'change': round(change, 2),
            'changePercent': round(change_percent, 2)
        }
    except Exception as e:
        print(f"❌ Error obteniendo índice IBEX: {str(e)}")
        return None

def update_data():
    """
    Actualiza todos los datos y genera el archivo JSON
    """
    print("🚀 Iniciando actualización de datos del IBEX 35...")
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Obtener datos del índice
    print("\n📊 Obteniendo datos del índice IBEX 35...")
    index_data = get_ibex_index()
    
    # Obtener datos de cada empresa
    print(f"\n📈 Obteniendo datos de {len(IBEX_35_COMPANIES)} empresas...")
    companies_data = []
    
    for i, company in enumerate(IBEX_35_COMPANIES, 1):
        print(f"[{i}/{len(IBEX_35_COMPANIES)}] {company['name']} ({company['ticker']})...", end=' ')
        
        stock_data = get_stock_data(company['ticker'])
        
        if stock_data:
            companies_data.append({
                'name': company['name'],
                'ticker': company['ticker'].replace('.MC', ''),
                'sector': company['sector'],
                'price': stock_data['price'],
                'change': stock_data['change'],
                'marketCap': stock_data['marketCap']
            })
            print("✅")
        else:
            print("❌")
        
        # Pequeña pausa para no saturar la API
        time.sleep(0.5)
    
    # Preparar datos finales
    output_data = {
        'lastUpdate': datetime.now().isoformat(),
        'index': index_data if index_data else {
            'value': 0,
            'change': 0,
            'changePercent': 0
        },
        'companies': companies_data
    }
    
    # Guardar JSON
    output_file = 'ibex_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Datos actualizados exitosamente!")
    print(f"📁 Archivo generado: {output_file}")
    print(f"📊 Empresas procesadas: {len(companies_data)}/{len(IBEX_35_COMPANIES)}")
    
    return output_data

if __name__ == '__main__':
    try:
        update_data()
    except KeyboardInterrupt:
        print("\n\n⚠️  Actualización interrumpida por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error crítico: {str(e)}")
        raise
