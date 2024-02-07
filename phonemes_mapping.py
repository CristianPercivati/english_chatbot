arpa_to_ipa = {
        'AO': 'ɔ', 'AO0': 'ɔ','AO1': 'ɔ','AO2': 'ɔ',
        'AA': 'ɑ','AA0': 'ɑ','AA1': 'ɑ','AA2': 'ɑ',
        'IY': 'i','IY0': 'i','IY1': 'i','IY2': 'i',
        'UW': 'u','UW0': 'u','UW1': 'u','UW2': 'u',
        'EH': 'e','EH0': 'e','EH1': 'e','EH2': 'e',
        'IH': 'ɪ','IH0': 'ɪ','IH1': 'ɪ','IH2': 'ɪ',
        'UH': 'ʊ','UH0': 'ʊ','UH1': 'ʊ','UH2': 'ʊ',
        'AH': 'ʌ','AH0': 'ə','AH1': 'ʌ','AH2': 'ʌ',
        'AE': 'æ','AE0': 'æ','AE1': 'æ','AE2': 'æ',
        'AX': 'ə','AX0': 'ə','AX1': 'ə','AX2': 'ə',
        'EY': 'eɪ','EY0': 'eɪ','EY1': 'eɪ','EY2': 'eɪ',
        'AY': 'aɪ','AY0': 'aɪ','AY1': 'aɪ','AY2': 'aɪ',
        'OW': 'oʊ','OW0': 'oʊ','OW1': 'oʊ','OW2': 'oʊ',
        'AW': 'aʊ','AW0': 'aʊ','AW1': 'aʊ','AW2': 'aʊ',
        'OY': 'ɔɪ','OY0': 'ɔɪ','OY1': 'ɔɪ','OY2': 'ɔɪ',
        'P': 'p','B': 'b','T': 't','D': 'd','K': 'k','G': 'g',
        'CH': 'tʃ','JH': 'dʒ','F': 'f','V': 'v','TH': 'θ','DH': 'ð',
        'S': 's','Z': 'z','SH': 'ʃ','ZH': 'ʒ','HH': 'h','M': 'm','N': 'n',
        'NG': 'ŋ','L': 'l','R': 'r',
        'ER': 'ɜr','ER0': 'ɜr','ER1': 'ɜr','ER2': 'ɜr',
        'AXR': 'ər','AXR0': 'ər','AXR1': 'ər','AXR2': 'ər',
        'W': 'w','Y': 'j',
    }

consonantes = ['P', 'B', 'T', 'D', 'K', 'G', 'F', 'V', 'S', 'Z', 'HH', 
                   'M', 'N', 'L', 'R', 'W', 'Y']
consonantes_comp = ['CH', 'JH', 'TH', 'DH', 'SH', 'Z', 'NG']
vocales_comp = ['AA0', 'AA1', 'AA2',    # /ɑ/
                'AE0', 'AE1', 'AE2',    # /æ/
                'AH0', 'AH1', 'AH2',    # /ʌ/ or /ə/
                'AO0', 'AO1', 'AO2',    # /ɔ/
                'AW0', 'AW1', 'AW2',    # /aʊ/
                'AY0', 'AY1', 'AY2',    # /aɪ/
                'EH0', 'EH1', 'EH2',    # /ɛ/
                'ER0', 'ER1', 'ER2',    # /ɝ/ or /ɚ/
                'EY0', 'EY1', 'EY2',    # /eɪ/
                'IH0', 'IH1', 'IH2',    # /ɪ/
                'IY0', 'IY1', 'IY2',    # /i/
                'OW0', 'OW1', 'OW2',    # /oʊ/
                'OY0', 'OY1', 'OY2',    # /ɔɪ/
                'UH0', 'UH1', 'UH2',    # /ʊ/
                'UW0', 'UW1', 'UW2',    # /u/
                'UX0', 'UX1', 'UX2',    # /u/
                'IX0', 'IX1', 'IX2',    # /ɨ/
                'AX0', 'AX1', 'AX2',    # /ə/
                'IX0', 'IX1', 'IX2'     # /ɨ/
               ]