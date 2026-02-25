import re

# Eredeti fájl beolvasása
with open('magyarorszag_terkep.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Új CSS színek - vagány, neon, sötét téma
new_css = """<style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Inter', system-ui, sans-serif; 
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh; 
            padding: 20px;
            color: #fff;
        }
        
        .container { 
            max-width: 1400px; 
            margin: 0 auto; 
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border-radius: 24px; 
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1); 
            padding: 40px; 
        }
        
        h1 { 
            text-align: center; 
            font-size: 3em; 
            margin-bottom: 10px;
            background: linear-gradient(135deg, #00f5ff 0%, #b829dd 50%, #ff006e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
            letter-spacing: -1px;
        }
        
        .subtitle {
            text-align: center;
            color: rgba(255,255,255,0.6);
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        
        .game-info { 
            display: flex; 
            justify-content: center; 
            gap: 30px; 
            margin-bottom: 30px; 
            flex-wrap: wrap; 
        }
        
        .info-box { 
            background: linear-gradient(135deg, rgba(0,245,255,0.15) 0%, rgba(184,41,221,0.15) 100%);
            border: 1px solid rgba(0,245,255,0.3);
            color: white; 
            padding: 20px 40px; 
            border-radius: 16px; 
            font-size: 1em; 
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3), 0 0 20px rgba(0,245,255,0.1);
            transition: transform 0.3s ease;
        }
        
        .info-box:hover { transform: translateY(-5px); }
        
        .info-box span { 
            font-size: 2em; 
            display: block; 
            margin-top: 8px;
            background: linear-gradient(135deg, #00f5ff 0%, #ff006e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        
        .question-box { 
            text-align: center; 
            background: rgba(0,0,0,0.3);
            border-radius: 20px; 
            padding: 30px; 
            margin-bottom: 25px; 
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.3);
        }
        
        .question-label { 
            color: rgba(255,255,255,0.6); 
            font-size: 1em; 
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .question-county { 
            color: #00f5ff;
            font-size: 2.8em; 
            font-weight: 800;
            text-shadow: 0 0 30px rgba(0,245,255,0.5);
            letter-spacing: -1px;
        }
        
        .map-container { 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            background: rgba(0,0,0,0.2);
            border-radius: 20px; 
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.05);
        }
        
        svg { 
            width: 100%; 
            max-width: 1100px; 
            height: auto;
            filter: drop-shadow(0 10px 40px rgba(0,0,0,0.5));
        }

        .county { 
            fill: url(#countyGradient);
            stroke: rgba(255,255,255,0.4); 
            stroke-width: 1.5; 
            stroke-linejoin: round; 
            cursor: pointer; 
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .county:hover { 
            fill: url(#countyHoverGradient);
            stroke: #00f5ff;
            stroke-width: 3;
            filter: drop-shadow(0 0 15px rgba(0,245,255,0.6));
        }

        .county.correct { 
            fill: url(#correctGradient) !important;
            stroke: #39ff14 !important;
            stroke-width: 3 !important;
            filter: drop-shadow(0 0 20px rgba(57,255,20,0.8));
            animation: pulse-correct 0.6s ease;
        }

        .county.wrong { 
            fill: url(#wrongGradient) !important;
            stroke: #ff006e !important;
            stroke-width: 3 !important;
            filter: drop-shadow(0 0 15px rgba(255,0,110,0.6));
            animation: shake 0.5s ease;
        }

        .county.highlight-correct { 
            fill: url(#correctGradient) !important;
            stroke: #39ff14 !important;
            stroke-width: 3 !important;
            filter: drop-shadow(0 0 25px rgba(57,255,20,0.9));
            animation: pulse 1s ease infinite;
        }

        .county.disabled { 
            pointer-events: none; 
            opacity: 0.4;
            filter: grayscale(0.8);
        }

        @keyframes pulse-correct { 
            0%, 100% { transform: scale(1); } 
            50% { transform: scale(1.03); } 
        }
        
        @keyframes shake { 
            0%, 100% { transform: translateX(0); } 
            25% { transform: translateX(-8px); } 
            75% { transform: translateX(8px); } 
        }
        
        @keyframes pulse { 
            0%, 100% { opacity: 1; filter: drop-shadow(0 0 20px rgba(57,255,20,0.8)); } 
            50% { opacity: 0.7; filter: drop-shadow(0 0 30px rgba(57,255,20,1)); } 
        }

        .balaton { 
            fill: url(#balatonGradient);
            stroke: #00d4ff; 
            stroke-width: 1.5;
            pointer-events: none;
            filter: drop-shadow(0 0 10px rgba(0,212,255,0.5));
        }

        .feedback { 
            text-align: center; 
            margin-top: 25px; 
            padding: 25px; 
            border-radius: 20px; 
            font-size: 1.4em; 
            font-weight: 700;
            opacity: 0; 
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            transform: translateY(10px);
            border: 2px solid transparent;
        }
        
        .feedback.show { 
            opacity: 1;
            transform: translateY(0);
        }
        
        .feedback.correct { 
            background: linear-gradient(135deg, rgba(57,255,20,0.15) 0%, rgba(0,245,255,0.15) 100%);
            color: #39ff14;
            border-color: rgba(57,255,20,0.5);
            box-shadow: 0 0 30px rgba(57,255,20,0.2);
            text-shadow: 0 0 20px rgba(57,255,20,0.5);
        }
        
        .feedback.wrong { 
            background: linear-gradient(135deg, rgba(255,0,110,0.15) 0%, rgba(255,140,0,0.15) 100%);
            color: #ff006e;
            border-color: rgba(255,0,110,0.5);
            box-shadow: 0 0 30px rgba(255,0,110,0.2);
            text-shadow: 0 0 20px rgba(255,0,110,0.5);
        }

        .next-btn, .restart-btn { 
            display: none; 
            margin: 25px auto 0; 
            padding: 18px 50px; 
            background: linear-gradient(135deg, #00f5ff 0%, #b829dd 100%);
            color: #0f0c29; 
            border: none; 
            border-radius: 16px; 
            font-size: 1.2em; 
            font-weight: 800;
            cursor: pointer;
            box-shadow: 0 10px 40px rgba(0,245,255,0.4);
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .next-btn:hover, .restart-btn:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 15px 50px rgba(0,245,255,0.6);
        }
        
        .next-btn.show { display: block; }

        .modal-overlay { 
            display: none; 
            position: fixed; 
            top: 0; left: 0; 
            width: 100%; height: 100%; 
            background: rgba(0,0,0,0.8);
            backdrop-filter: blur(10px);
            z-index: 1000; 
            justify-content: center; 
            align-items: center; 
        }
        
        .modal-overlay.show { display: flex; animation: fadeIn 0.3s ease; }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .results-modal { 
            background: linear-gradient(135deg, rgba(15,12,41,0.95) 0%, rgba(48,43,99,0.95) 100%);
            border-radius: 30px; 
            padding: 50px; 
            max-width: 500px; 
            width: 90%; 
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 25px 50px rgba(0,0,0,0.5), 0 0 50px rgba(0,245,255,0.1);
            animation: slideUp 0.5s ease;
        }
        
        @keyframes slideUp {
            from { transform: translateY(30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .results-modal h2 { 
            font-size: 2.2em; 
            margin-bottom: 25px;
            background: linear-gradient(135deg, #00f5ff 0%, #ff006e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
        
        .score-display { 
            font-size: 5em; 
            font-weight: 800;
            background: linear-gradient(135deg, #00f5ff 0%, #b829dd 50%, #ff006e 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 25px 0;
        }
        
        .score-text { 
            color: rgba(255,255,255,0.7); 
            font-size: 1.4em; 
            margin-bottom: 30px;
            font-weight: 600;
        }
        
        .result-message { 
            padding: 20px; 
            border-radius: 16px; 
            margin-bottom: 30px; 
            font-weight: 700;
            font-size: 1.1em;
            border: 2px solid transparent;
        }
        
        .result-message.excellent { 
            background: linear-gradient(135deg, rgba(57,255,20,0.15) 0%, rgba(0,245,255,0.15) 100%);
            color: #39ff14;
            border-color: rgba(57,255,20,0.4);
            box-shadow: 0 0 30px rgba(57,255,20,0.2);
        }
        
        .result-message.good { 
            background: linear-gradient(135deg, rgba(0,245,255,0.15) 0%, rgba(184,41,221,0.15) 100%);
            color: #00f5ff;
            border-color: rgba(0,245,255,0.4);
            box-shadow: 0 0 30px rgba(0,245,255,0.2);
        }
        
        .result-message.okay { 
            background: linear-gradient(135deg, rgba(255,140,0,0.15) 0%, rgba(255,0,110,0.15) 100%);
            color: #ff8c00;
            border-color: rgba(255,140,0,0.4);
            box-shadow: 0 0 30px rgba(255,140,0,0.2);
        }
        
        .result-message.practice { 
            background: linear-gradient(135deg, rgba(255,0,110,0.15) 0%, rgba(255,0,0,0.15) 100%);
            color: #ff006e;
            border-color: rgba(255,0,110,0.4);
            box-shadow: 0 0 30px rgba(255,0,110,0.2);
        }
    </style>"""

# SVG gradientek hozzáadása
svg_gradients = """<svg viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="countyGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#b829dd;stop-opacity:0.9" />
                        <stop offset="100%" style="stop-color:#5a189a;stop-opacity:0.9" />
                    </linearGradient>
                    <linearGradient id="countyHoverGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#00f5ff;stop-opacity:0.9" />
                        <stop offset="100%" style="stop-color:#b829dd;stop-opacity:0.9" />
                    </linearGradient>
                    <linearGradient id="correctGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#39ff14;stop-opacity:0.9" />
                        <stop offset="100%" style="stop-color:#00d4ff;stop-opacity:0.9" />
                    </linearGradient>
                    <linearGradient id="wrongGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#ff006e;stop-opacity:0.9" />
                        <stop offset="100%" style="stop-color:#ff8c00;stop-opacity:0.9" />
                    </linearGradient>
                    <linearGradient id="balatonGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#00d4ff;stop-opacity:0.8" />
                        <stop offset="50%" style="stop-color:#0099cc;stop-opacity:0.9" />
                        <stop offset="100%" style="stop-color:#0066aa;stop-opacity:0.8" />
                    </linearGradient>
                </defs>"""

# Cseréljük ki a CSS-t
content = re.sub(r'<style>.*?</style>', new_css, content, flags=re.DOTALL)

# Cseréljük ki az SVG-t a gradientekkel
content = re.sub(r'<svg viewBox="0 0 1200 800" xmlns="http://www\.w3\.org/2000/svg">', svg_gradients, content)

# Adjuk hozzá a subtitle-t a h1 után
content = content.replace('<h1>🗺️ Magyarország Vármegye Kvíz</h1>', '<h1>🗺️ Magyarország Vármegye Kvíz</h1>\n        <p class="subtitle">Találd meg a helyes vármegyét a térképen!</p>')

# Mentés
with open('magyarorszag_terkep.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Kész! A fájl frissítve vagány színekkel!')
