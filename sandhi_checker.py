import ilakkanam
import letters
import collections
import codecs
import os
import sys

mei_letters = ilakkanam.mei_letters
uyir_letters = ilakkanam.uyir_letters
kuril_letters = ilakkanam.kuril_letters
nedil_letters = ilakkanam.nedil_letters
agaram_letters = ilakkanam.agaram_letters
uyirmei_letters = ilakkanam.uyirmei_letters
vallinam_letters = ilakkanam.vallinam_letters
mellinam_letters = ilakkanam.mellinam_letters
tamil_letters = ilakkanam.tamil_letters
sanskrit_letters = ilakkanam.sanskrit_letters 
sanskrit_mei_letters = ilakkanam.sanskrit_mei_letters 
ayudha_letter = letters.ayudha_letter
special_chars = letters.special_chars
one_letter_words=letters.one_letter_words
suttu_vina= letters.suttu_vina
numerals=letters.numerals
viyankol= letters.viyankol
special_chars=letters.special_chars
one_letter_words=letters.one_letter_words
numbers=letters.numbers
granda = letters.granda
english = letters.english 
suttu_vina_not = letters.suttu_vina
specific_words = letters.specific_words

assert( len(english) == 52 )

def safe_splitMeiUyir(arg):
    try:
        # when uyir letters are passed to splitMeiUyir function it will throw an IndexError
        rval = ilakkanam.splitMeiUyir(arg)
        if not isinstance(rval,tuple):
            if rval in uyir_letters:
                return (u'',rval)
            return (rval,u'')
        return rval
    except IndexError as idxerr:
        pass
    except ValueError as valerr:
        pass
    return (u'',u'')

def check_sandhi(words):
    if not isinstance(words,list):
        words = ilakkanam.get_words(words)

    # This is for storing the results
    fixed_list=[]
    result = []

    for counter,word in enumerate(words):
        next_word = (counter+1) < len(words) and words[counter+1] or u' '
        
        # letters is basically a list of characters of a word
        letters = ilakkanam.get_letters(word)
        # வல்லினம் மிகா வந்த, கண்ட, சொன்ன, வரும் என்பன  போன்ற பெயரெச்சங்களோடு படி, ஆறு என்னும் சொற்கள்- கண்டவாறு சொன்னான்
        if (ilakkanam.get_letters(word)[0]) in [u'வ',u'க',u'சொ']:
            if (ilakkanam.get_letters(word)[-1]) in [u'டி',u'று']:
                fixed_list.append(word)
                # if _DEBUG: print(u"மிகா - விதி 3 - " + word)
                result.append(word) #u'விதி 3',u'மிகா
                continue

        # வல்லினம் மிகா எண்ணுப்பெயர்கள் - ஐந்து சிறுவர்கள்
        if word in numerals:
            fixed_list.append(word)
            # if _DEBUG: print(u"மிகா - விதி 4 - " + word)
            result.append(word) #u'விதி 4',u'மிகா
            continue

        # ஓர் எழுத்துச் சொற்கள் முன் வல்லினம் மிகல்
        # 6.1.2 - கை குழந்தை
        if len(ilakkanam.get_letters(word)) == 1:
            if  word in one_letter_words:
                first_char_of_next_word = (next_word[0])
                mei_of_first_char_of_next_word = safe_splitMeiUyir(first_char_of_next_word)[0]
                fixed_list.append(word + mei_of_first_char_of_next_word)
                # if _DEBUG: print(u"மிகும் - விதி 1 - " + word + mei_of_first_char_of_next_word)
                result.append(word) #u'விதி 1',u'மிகும்
            continue

        # வல்லினம் மிகா ஒடு & ஓடு என உயிர் ஈறு கொண்டவை - கத்தியோடு நின்றான்
        if (safe_splitMeiUyir(ilakkanam.get_letters(word)[-2])[1]) in [u'ஒ',u'ஓ']:
            if (ilakkanam.get_letters(word)[-1]) == u'டு':
                fixed_list.append(word)
                # if _DEBUG: print(u"மிகா - விதி 5 - " + word)
                result.append(word) #u'விதி 5',u'மிகா
                continue

        # வல்லினம் மிகா ‘கொண்டு’ என்னும் சொல்லுருபு -கத்திகொண்டு குத்தினான்
        if u''.join(ilakkanam.get_letters(word)[-3:]) ==  u'கொண்டு':
            fixed_list.append(word)
            # if _DEBUG: print(u"மிகா - விதி 6 - " + word)
            result.append(word) #u'விதி 6',u"மிகா")
            continue

        # வல்லினம் மிகா இல் என்பதோடு இருந்து என்னும்  சொல்லுருபு - வீட்டிலிருந்து சென்றான்
        if u''.join(ilakkanam.get_letters(word)[-4:]) == u'லிருந்து':
            fixed_list.append(word)
            # if _DEBUG: print(u"மிகா - விதி 7 - " + word)
            result.append(word) #u'விதி 7',u"மிகா")
            continue

        # வல்லினம் மிகா இன் என்பதோடு நின்று என்னும் சொல்லுருபு - வீட்டினின்று வெளியேறினான்
        if u''.join(ilakkanam.get_letters(word)[-3:]) == u'னின்று':
            fixed_list.append(word)
            # if _DEBUG: print(u"மிகா - விதி 8 - " + word)
            result.append(word) #u'விதி 8',u"மிகா")
            continue

        # வல்லினம் மிகா ஆறாம் வேற்றுமைக்கு உரிய அது - எனது புத்தகம்
        if (safe_splitMeiUyir(ilakkanam.get_letters(word)[-2])[1]) == u'அ':
            if (ilakkanam.get_letters(word)[-1]) == u'து':
                fixed_list.append(word)
                # if _DEBUG: print(u"மிகா - விதி 9 - " + word)
                result.append(word) #u'விதி 9',u'மிகா
                continue

       # வல்லினம் மிகா இடங்கள்
        if ilakkanam.get_letters(word)[-1] in special_chars:
            fixed_list.append(word)
            result.append(word) #u'விதி 1',u'மிகா
            continue

        # வல்லினம் மிகா சுட்டு, வினா அடியாகத் தோன்றிய சொற்கள் - எத்தனை பழங்கள்?
        # ‘அஃறிணைப் பன்மை’ - பல பசு
        if word in suttu_vina_not:
            fixed_list.append(word)
            # if _DEBUG: print(u"மிகா - விதி 2 - " + word)
            result.append(word) #u'விதி 2',u'மிகா
            continue

        

        # வல்லினம் மிகா மென்தொடர்க் குற்றியலுகர  வினையெச்சங்கள் - ண்டு, ந்து, ன்று என முடியும் -கண்டு பேசினார்
        # இடைத்தொடர்க் குற்றியலுகர  வினையெச்சங்கள் - ய்து என முடியும் - செய்து தந்தான்
        if ''.join(ilakkanam.get_letters(word)[-2:]) in [u'ண்டு',u'ந்து',u'ன்று',u'ய்து',u'ன்கு']:            
            fixed_list.append(word)
            # if _DEBUG: print(u"மிகா - Rule12 - " + word)
            counter = counter+1
            result.append(word) #u'விதி 12',u'மிகா
            continue

        # கொன்று குவித்தான்
        if u''.join(ilakkanam.get_letters(word)[-2:]) == u'ன்று':
            fixed_list.append(word)
            # if _DEBUG: print(u"மிகா - Rule13 - " + word)
            counter = counter+1
            result.append(word) #u'விதி 13',u'மிகா
            continue

        # வல்லினம் மிகா இடைத்தொடர்க் குற்றியலுகர  வினையெச்சங்கள் - ய்து என முடியும்
        # செய்து தந்தான்
        if u''.join(ilakkanam.get_letters(word)[-2:]) == u'ய்து':
            fixed_list.append(word)
            # if _DEBUG: print(u"மிகா - Rule14 - " + word)
            result.append(word) #u'விதி 14',u'மிகா
            counter = counter+1
            continue

        # வல்லினம் மிகா மற்ற பெயரெச்சங்கள் - ஆத, இய, ஐய,ற்ற,ல்ல, ட்ட கின்ற, உம் ஆகிய விகுதிகள் பெற்று முடியும்
        # அழியாத கல்வி
        if u''.join(ilakkanam.get_letters(word)[-1:]) == u'த':
            if (safe_splitMeiUyir(ilakkanam.get_letters(word)[-2])[1]) == u'ஆ':
                fixed_list.append(word)
                # if _DEBUG: print(u"மிகா - Rule15 - " + word)
                result.append(word) #u'விதி 15',u'மிகா
                counter = counter+1
                continue

        # பெரிய பெண்
        if u''.join(ilakkanam.get_letters(word)[-1:]) == u'ய':
            if (safe_splitMeiUyir(ilakkanam.get_letters(word)[-2])[1]) == u'இ':
                fixed_list.append(word)
                # if _DEBUG: print(u"மிகா - Rule16 - " + word)
                counter = counter+1
                result.append(word) #u'விதி 16',u'மிகா
                continue

        # கற்ற சிறுவன் 
        if ''.join(ilakkanam.get_letters(word)[-2:]) in [u'ற்ற',u'ல்ல',u'ட்ட',u'ன்ற',u'ந்த',u'த்து',u'இனி']:            
            fixed_list.append(word)
            # if _DEBUG: print(u"மிகா - Rule18 - " + word)
            result.append(word) #u'விதி 18',u'மிகா
            continue

        # வல்லினம் மிகா மற்ற வினையெச்சங்கள் - ஆக, அன, யுற,றகு,க்கு ஆகிய  விகுதிகள் பெற்று முடியும்  
        # அழியாத கல்வி 
        if len(ilakkanam.get_letters(word)) > 1:  
            if ''.join(ilakkanam.get_letters(word)[-1:]) == u'க': 
                if ''.join(ilakkanam.get_letters(word)[-2]) not in (uyir_letters + numbers + ayudha_letter + granda + special_chars + english):             
                    if (ilakkanam.splitMeiUyir(ilakkanam.get_letters(word)[-2])[1]) == u'ஆ':
                        fixed_list.append(word)
                        # if _DEBUG: print(u"மிகா - Rule19 - " + word)
                        result.append(word) #u'விதி 19',u'மிகா
                        continue
        if len(ilakkanam.get_letters(word)) > 1:  
            if ''.join(ilakkanam.get_letters(word)[-1]) == u'ன':  
                if ''.join(ilakkanam.get_letters(word)[-2]) not in (uyir_letters + numbers + ayudha_letter + granda + special_chars + english):               
                    if (ilakkanam.splitMeiUyir(ilakkanam.get_letters(word)[-2])[1]) == u'அ':
                        fixed_list.append(word)
                        # if _DEBUG: print(u"மிகா - Rule20 - " + word)
                        result.append(word) #u'விதி 20',u'மிகா
                        continue

        if ''.join(ilakkanam.get_letters(word)[-2:]) in [u'யுற',u'றகு',u'ற்கு',u'க்கு',u'போது']:            
                fixed_list.append(word)
                # if _DEBUG: print(u"மிகா - Rule21 - " + word)
                result.append(word) #u'விதி 21',u'மிகா
                continue
      
        # வல்லினம் மிகா இரட்டைக் கிளவி, அடுக்குத்தொடர்கள் - கல கல
        if word == next_word:
            fixed_list.append(word)
            # if _DEBUG: print(u"மிகா - Rule22 - " + word)
            result.append(word) #u'விதி 22',u'மிகா
            continue
        
        # வல்லினம் மிகா வியங்கோள் வினைமுற்று - வருக புலவரே
        if word in viyankol:
            fixed_list.append(word)
            # if _DEBUG: print(u"மிகா - Rule23 - " + word)
            result.append(word) #u'விதி 23',u'மிகா
            continue
        
        
        if (safe_splitMeiUyir(ilakkanam.get_letters(word)[-1])[1]) == u'இ':
            first_char_of_next_word = (next_word[0])
            mei_of_first_char_of_next_word = safe_splitMeiUyir(first_char_of_next_word)[0]
            fixed_list.append(word + mei_of_first_char_of_next_word)
            # if _DEBUG: print(u"மிகும் - விதி 11 - " + word + mei_of_first_char_of_next_word)
            result.append(word) #u'விதி 11',u'மிகும்
            continue

        if (safe_splitMeiUyir(ilakkanam.get_letters(word)[-1])) == u'ய்':
            first_char_of_next_word = (next_word[0])
            mei_of_first_char_of_next_word = safe_splitMeiUyir(first_char_of_next_word)[0]
            fixed_list.append(word + mei_of_first_char_of_next_word)
            # if _DEBUG: print(u"மிகும் - விதி 12 - " + word + mei_of_first_char_of_next_word)
            result.append(word) #u'விதி 12',u'மிகும்
            continue

        if (safe_splitMeiUyir(ilakkanam.get_letters(word)[-1])) == u'ர்':
            first_char_of_next_word = (next_word[0])
            mei_of_first_char_of_next_word = safe_splitMeiUyir(first_char_of_next_word)[0]
            fixed_list.append(word + mei_of_first_char_of_next_word)
            # if _DEBUG: print(u"மிகும் - விதி 13 - " + word + mei_of_first_char_of_next_word)
            result.append(word) #u'விதி 13',u'மிகும்
            continue

        if (safe_splitMeiUyir(ilakkanam.get_letters(word)[-1])[1]) == u'ஆ':
            first_char_of_next_word = (next_word[0])
            mei_of_first_char_of_next_word = safe_splitMeiUyir(first_char_of_next_word)[0]
            fixed_list.append(word + mei_of_first_char_of_next_word)
            # if _DEBUG: print(u"மிகும் - விதி 14 - " + word + mei_of_first_char_of_next_word)
            result.append(word) #u'விதி 14',u'மிகும்
            continue

        # வல்லினம் மிகா பல, சில, ஏவல் வினை - வா கலையரசி
        if word in [u'கல',u'பல',u'சில',u'வா',u'எழு',u'போ',u'பார்'] :
            fixed_list.append(word)
            # if _DEBUG: print(u"மிகா - Rule26 - " + word)
            counter = counter+1
            result.append(word) #u'விதி 26',u'மிகா
            continue

        # 6.1.1 சுட்டு, வினா அடியாகத் தோன்றிய சொற்கள் முன் வல்லினம் மிகல் - அந்த பையன்
        if (ilakkanam.get_letters(word)) in suttu_vina:
            if (ilakkanam.get_letters(word)[-1]) not in mei_letters:
                if ''.join(ilakkanam.get_letters(word)[1:3]) == u'வ்வா':
                    fixed_list.append(word)
                    # if _DEBUG: print(u"மிகா - Rule25 - " + word)
                    result.append(word) #u'விதி 25',u'மிகா
                    continue  
                if ''.join(ilakkanam.get_letters(word)[-2:]) != u'டைய':
                    first_char_of_next_word = (next_word[0])
                    # if _DEBUG: print(u"மிகா - Rule29 - " + word)
                    result.append(word) #u'விதி 29',u'மிகா
                    counter = counter+1
                    continue
                if u''.join(ilakkanam.get_letters(word)[-2:]) != u'டைய':
                    first_char_of_next_word = (next_word[0])
                    if first_char_of_next_word not in (uyir_letters + numbers + ayudha_letter + granda + special_chars + english):
                        mei_of_first_char_of_next_word = safe_splitMeiUyir(first_char_of_next_word)[0]
                        if mei_of_first_char_of_next_word in vallinam_letters:
                            fixed_list.append(word + mei_of_first_char_of_next_word)
                            # if _DEBUG: print(u"மிகும் - Rule2 - " + word + mei_of_first_char_of_next_word)
                            result.append(word) #u'விதி 2',u'மிகும்
                            continue  

        # 6.1.3 - 1 வன்தொடர்க் குற்றியலுகரம் முன் வல்லினம் மிகல் - கற்று கொடுத்தான் 
        if len(ilakkanam.get_letters(word)) > 1:        
            if (ilakkanam.get_letters(word)[-2]) in vallinam_letters:
                uyir_of_last_char = safe_splitMeiUyir(ilakkanam.get_letters(word)[-1])[1]
                if uyir_of_last_char == u'உ':                
                    first_char_of_next_word = (next_word[0])
                    if first_char_of_next_word not in (uyir_letters + numbers + ayudha_letter + granda + special_chars + english):
                        mei_of_first_char_of_next_word = safe_splitMeiUyir(first_char_of_next_word)[0]
                        if mei_of_first_char_of_next_word in vallinam_letters:                    
                            fixed_list.append(word + mei_of_first_char_of_next_word)   
                            # if _DEBUG: print(u"மிகும் - Rule3 - " + word + mei_of_first_char_of_next_word)
                            result.append(word) #u'விதி 3',u'மிகும்
                            continue

        # வன்தொடர்க் குற்றியலுகரம் முன் வல்லினம் மிகல் - கற்று கொடுத்தான்
        # 6.1.3 - 1

        if (ilakkanam.get_letters(word)[-2]) in vallinam_letters:
            uyir_of_last_char = safe_splitMeiUyir(ilakkanam.get_letters(word)[-1])[1]

            if uyir_of_last_char == u'உ':

                first_char_of_next_word = (next_word[0])
                mei_of_first_char_of_next_word = safe_splitMeiUyir(first_char_of_next_word)[0]
                fixed_list.append(word + mei_of_first_char_of_next_word)
                # if _DEBUG: print(u"மிகும் - விதி 3 - " + word + mei_of_first_char_of_next_word)
                result.append(word) #u'விதி 3',u'மிகும்
                continue

            

        # இன்றைய செய்தி
        if u''.join(ilakkanam.get_letters(word)[-1:]) == u'ய':
            if (safe_splitMeiUyir(ilakkanam.get_letters(word)[-2])[1]) == u'ஐ':
                fixed_list.append(word)
                # if _DEBUG: print(u"மிகா - Rule17 - " + word)
                result.append(word) #u'விதி 17',u'மிகா
                counter = counter+1
                continue
        # வல்லினம் மிகா ‘உடைய’ என்னும் சொல்லுருபு- என்னுடைய புத்தகம்
        if u''.join(ilakkanam.get_letters(word)[-2:]) == u'டைய':
            if (safe_splitMeiUyir(ilakkanam.get_letters(word)[-3])[1]) == u'உ':
                fixed_list.append(word)
                # if _DEBUG: print(u"மிகா - விதி 10 - " + word)
                result.append(word) #u'விதி 10',u'மிகா
                continue
        # வல்லினம் மிகா மென்தொடர்க் குற்றியலுகர  வினையெச்சங்கள் - ண்டு, ந்து, ன்று என முடியும்
        # கண்டு பேசினார்
        if u''.join(ilakkanam.get_letters(word)[-2:]) == u'ண்டு':
            fixed_list.append(word)
            # if _DEBUG: print(u"மிகா - Rule11 - " + word)
            counter = counter+1
            result.append(word) #u'விதி 11',u'மிகா
            continue

        # 6.1.5 - 1 - இரண்டாம் வேற்றுமை விரி - கனியை  தின்றான்
        if (safe_splitMeiUyir(ilakkanam.get_letters(word)[-1])[1]) == u'ஐ':
            first_char_of_next_word = (next_word[0])
            mei_of_first_char_of_next_word = safe_splitMeiUyir(first_char_of_next_word)[0]
            fixed_list.append(word + mei_of_first_char_of_next_word)
            # if _DEBUG: print(u"மிகும் - விதி 8 - " + word + mei_of_first_char_of_next_word)
            result.append(word) #u'விதி 8',u'மிகும்
            continue

        # 6.1.5 - 2 -  நான்காம் வேற்றுமை விரி - எனக்கு  கொடு
        if ilakkanam.get_letters(word)[-1] == u'கு':
            first_char_of_next_word = (next_word[0])
            mei_of_first_char_of_next_word = safe_splitMeiUyir(first_char_of_next_word)[0]
            fixed_list.append(word + mei_of_first_char_of_next_word)
            # if _DEBUG: print(u"மிகும் - விதி 9 - " + word + mei_of_first_char_of_next_word)
            result.append(word) #u'விதி 9',u'மிகும்
            continue

        # முற்றியலுகரச் சொற்கள் முன் வல்லினம் மிகல்
        # 6.1.4 - 1 - தனிக் குறில் அடுத்து வரும் உகரம்  - பொது பணி
        if len(ilakkanam.get_letters(word)) == 2:
            if (safe_splitMeiUyir(ilakkanam.get_letters(word)[-2])[1]) in kuril_letters:
                uyir_of_last_char = safe_splitMeiUyir(ilakkanam.get_letters(word)[-1])[1]
                if uyir_of_last_char == u'உ':
                    first_char_of_next_word = (next_word[0])
                    mei_of_first_char_of_next_word = safe_splitMeiUyir(first_char_of_next_word)[0]
                    fixed_list.append(word + mei_of_first_char_of_next_word)
                    # if _DEBUG: print(u"மிகும் - விதி 5 - " + word + mei_of_first_char_of_next_word)
                    result.append(word) #u'விதி 5',u'மிகும்
                    continue

        # உயிர்த்தொடர்க் குற்றியலுகரம் முன் வல்லினம் மிகல் - விறகு கடை
        # 6.1.3 - 3
        if safe_splitMeiUyir(ilakkanam.get_letters(word)[-2])[1] in uyir_letters:
            uyir_of_last_char = safe_splitMeiUyir(ilakkanam.get_letters(word)[-1])[1]

            if uyir_of_last_char == u'உ':
                first_char_of_next_word = (next_word[0])
                mei_of_first_char_of_next_word = safe_splitMeiUyir(first_char_of_next_word)[0]
                fixed_list.append(word + mei_of_first_char_of_next_word)
                # if _DEBUG: print(u"மிகும் - விதி 6 - " + word + mei_of_first_char_of_next_word)
                result.append(word) #u'விதி 6',u'மிகா
                continue

        # 6.1.4 - 1 - வல்லினமெய் அல்லாத பிற மெய்களின் மேல் ஏறி வருகின்ற உகரம் - தேர்வு கட்டணம்
        if (safe_splitMeiUyir(ilakkanam.get_letters(word)[-1])[0]) not in [u'க்',u'ச்',u'ட்',u'த்',u'ப்',u'ற்']:
            if (safe_splitMeiUyir(ilakkanam.get_letters(word)[-1])[1]) == u'உ':
                first_char_of_next_word = (next_word[0])
                mei_of_first_char_of_next_word = safe_splitMeiUyir(first_char_of_next_word)[0]
                fixed_list.append(word + mei_of_first_char_of_next_word)
                # if _DEBUG: print(u"மிகும் - விதி 7 - " + word + mei_of_first_char_of_next_word)
                result.append(word) #u'விதி 7',u'மிகும்
                continue

        
        
        

        fixed_list.append(word)
    return fixed_list,result
