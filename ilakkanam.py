import abc
import letters
import operator
import re
import string
from copy import copy
from sys import version

import functools

## constants
TA_ACCENT_LEN = 13  # 12 + 1
TA_AYUDHA_LEN = 1
TA_UYIR_LEN = 12
TA_MEI_LEN = 18
TA_AGARAM_LEN = 18
TA_SANSKRIT_LEN = 6
TA_UYIRMEI_LEN = 216
TA_GRANTHA_UYIRMEI_LEN = 24 * 12
TA_LETTERS_LEN = 247 + 6 * 12 + 22 + 4 - TA_AGARAM_LEN - 4  # 323


# List of letters you can use
uyir_letters = ["அ", "ஆ", "இ", "ஈ", "உ", "ஊ", "எ", "ஏ", "ஐ", "ஒ", "ஓ", "ஔ"]
vowel_a = "அ"
vowel_aa = "ஆ"
vowel_i = "இ"
vowel_ii = "ஈ"
vowel_u = "உ"
vowel_uu = "ஊ"
vowel_e = "எ"
vowel_ee = "ஏ"
vowel_ai = "ஐ"
vowel_o = "ஒ"
vowel_oo = "ஓ"
vowel_au = "ஔ"
aytham_letter = "ஃ"
ayudha_letter = aytham_letter

kuril_letters = letters.kuril_letters
nedil_letters = letters.nedil_letters
dipthong_letters = letters.dipthong_letters

pronoun_letters = letters.pronoun_letters
suttezhuththu = pronoun_letters

questionsuffix_letters = ["ஆ", "ஏ", "ஓ"]
vinaaezhuththu = questionsuffix_letters

vallinam_letters = ["க்", "ச்", "ட்", "த்", "ப்", "ற்"]
mellinam_letters = ["ங்", "ஞ்", "ண்", "ந்", "ம்", "ன்"]
idayinam_letters = ["ய்", "ர்", "ல்", "வ்", "ழ்", "ள்"]

mei_letters=letters.mei_letters
accent_symbols = letters.accent_symbols

accent_aa = accent_symbols[1]
accent_i = accent_symbols[2]
accent_u = accent_symbols[3]
accent_uu = accent_symbols[4]
accent_e = accent_symbols[5]
accent_ee = accent_symbols[6]
accent_ai = accent_symbols[7]
accent_o = accent_symbols[8]
accent_oo = accent_symbols[9]
accent_au = accent_symbols[10]

pulli_symbols = ["்"]

agaram_letters=letters.agaram_letters
mayangoli_letters = letters.mayangoli_letters

consonant_ka = "க"
consonant_nga = "ங"
consonant_ca = "ச"
consonant_ja = "ஜ"
consonant_nya = "ஞ"
consonant_tta = "ட"
consonant_nna = "ண"
consonant_nnna = "ன"
consonant_ta = "த"
consonant_tha = "த"
consonant_na = "ந"
consonant_pa = "ப"
consonant_ma = "ம"
consonant_ya = "ய"
consonant_ra = "ர"
consonant_rra = "ற"
consonant_la = "ல"
consonant_lla = "ள"
consonant_llla = "ழ"
consonant_zha = "ழ"
consonant_va = "வ"

sanskrit_letters = ["ஶ", "ஜ", "ஷ", "ஸ", "ஹ", "க்ஷ"]
sanskrit_mei_letters = ["ஶ்", "ஜ்", "ஷ்", "ஸ்", "ஹ்", "க்ஷ்"]

grantha_mei_letters = copy(mei_letters)
grantha_mei_letters.extend(sanskrit_mei_letters)

grantha_agaram_letters = copy(agaram_letters)
grantha_agaram_letters.extend(sanskrit_letters)

uyirmei_letters=  letters.uyirmei_letters
tamil247 = [ayudha_letter]
tamil247.extend(uyir_letters)
tamil247.extend(mei_letters)
tamil247.extend(uyirmei_letters)

tamil_digit_1to10 = ["௦", "௧", "௨", "௩", "௪", "௫", "௬", "௭", "௮", "௯", "௰"]
tamil_digit_100 = "௱"
tamil_digit_1000 = "௲"

tamil_digits = [(num, digit)
                for num, digit in zip(range(0, 11), tamil_digit_1to10)]
tamil_digits.extend([(100, tamil_digit_100), (1000, tamil_digit_1000)])

# tamil symbols
_day = "௳"
_month = "௴"
_year = "௵"
_debit = "௶"
_credit = "௷"
_rupee = "௹"
_numeral = "௺"
_sri = "\u0bb6\u0bcd\u0bb0\u0bc0"  # SRI - ஶ்ரீ
_ksha = "\u0b95\u0bcd\u0bb7"  # KSHA - க்ஷ
_ksh = "\u0b95\u0bcd\u0bb7\u0bcd"  # KSH - க்ஷ்
_indian_rupee = "₹"
tamil_symbols=[_day,_month,_year,_debit,_credit,_rupee,_numeral,_sri,_ksha,_ksh,_indian_rupee,]
## total tamil letters in use, including sanskrit letters
tamil_letters= letters.tamil_letters
grantha_uyirmei_letters = copy(tamil_letters[tamil_letters.index("கா") - 1:])

## length of the definitions
def accent_len():
    return TA_ACCENT_LEN  ## 13 = 12 + 1

def ayudha_len():
    return TA_AYUDHA_LEN  ## 1

def uyir_len():
    return TA_UYIR_LEN  ##12

def mei_len():
    return TA_MEI_LEN  ##18

def agaram_len():
    return TA_AGARAM_LEN  ##18

def uyirmei_len():
    return TA_UYIRMEI_LEN  ##216

def tamil_len():
    return len(tamil_letters)

## access the letters
def uyir(idx):
    assert idx >= 0 and idx < uyir_len()
    return uyir_letters[idx]


def agaram(idx):
    assert idx >= 0 and idx < agaram_len()
    return agaram_letters[idx]


def mei(idx):
    assert idx >= 0 and idx < mei_len()
    return mei_letters[idx]


def uyirmei(idx):
    assert idx >= 0 and idx < uyirmei_len()
    return uyirmei_letters[idx]

def uyirmei_constructed(mei_idx, uyir_idx):
    """ construct uyirmei letter give mei index and uyir index """
    idx, idy = mei_idx, uyir_idx
    assert idy >= 0 and idy < uyir_len()
    assert idx >= 0 and idx < 6 + mei_len()
    return grantha_agaram_letters[mei_idx] + accent_symbols[uyir_idx]


def tamil(idx):
    """ retrieve Tamil letter at canonical index from array utf8.tamil_letters """
    assert idx >= 0 and idx < tamil_len()
    return tamil_letters[idx]


# companion function to @tamil()
def getidx(letter):
    for itr in range(0, tamil_len()):
        if tamil_letters[itr] == letter:
            return itr
    raise Exception("Cannot find letter in Tamil arichuvadi")

def is_tamil_unicode_value(intx: int):
    return (intx >= (2946) and intx <= (3066))

def is_tamil_unicode_codept(x: str):
    intx = ord(x)
    return is_tamil_unicode_value(intx)

def is_tamil_unicode_predicate(x: str):
    if not is_tamil_unicode_codept(x[0]):
        return False
    return (len(x) > 1 and is_tamil_unicode_predicate(x[1:])) or True


def is_tamil_unicode(sequence):
    if isinstance(sequence, list):
        return list(map(is_tamil_unicode_predicate, sequence))
    if len(sequence) > 1:
        return list(map(is_tamil_unicode_predicate, get_letters(sequence)))
    return is_tamil_unicode_predicate(sequence)


def all_tamil(word_in):
    if isinstance(word_in, list):
        word = word_in
    else:
        word = get_letters(word_in)
    return all([(letter in tamil_letters) for letter in word])
    
_punctuation = '|'.join(re.escape(string.punctuation))
_whitespace_digits_or_alpha = re.compile(r'[\s|\d|'+_punctuation+']+')

def all_tamil_text(str):
    short_str = _whitespace_digits_or_alpha.sub('',str)
    return all_tamil(short_str)


def istamil(tchar):
    if tchar in tamil_letters:
        return True
    return False


def is_normalized(text):
    TLEN, idx = len(text), 1
    kaal = "ா"
    Laa = "ள"
    sinna_kombu, periya_kombu = "ெ", "ே"
    kombugal = [sinna_kombu, periya_kombu]

    # predicate measures if the normalization is violated
    def predicate(last_letter, prev_letter):
        if (kaal == last_letter) and (prev_letter in kombugal):
            return True
        if (Laa == last_letter) and (prev_letter == sinna_kombu):
            return True
        return False

    if TLEN < 2:
        return True
    elif TLEN == 2:
        if predicate(text[-1], text[-2]):
            return False
        return True
    idx = TLEN
    a = text[idx - 2]
    b = text[idx - 1]
    while idx >= 0:
        if predicate(b, a):
            return False
        b = a
        idx = idx - 1
        if idx >= 0:
            a = text[idx]
    return True


def _make_set(args):
    return frozenset(args)


grantha_agaram_set = _make_set(grantha_agaram_letters)
accent_symbol_set = _make_set(accent_symbols)
uyir_letter_set = _make_set(uyir_letters)

_GLL = set()
_GLL.update(uyir_letter_set)
_GLL.add(ayudha_letter)
_GLL.update(grantha_agaram_set)
## Split a tamil-unicode stream into
## tamil characters (individuals).
from functools import lru_cache


def copy_lru_decorator(f):
    @lru_cache(16192)
    def f_lru(*args, **kwargs):
        return f(*args, **kwargs)

    def f_copy_lru(*args, **kwargs):
        y = f_lru(*args, **kwargs)
        return copy(y)

    return f_copy_lru


# @copy_lru_decorator
def get_letters(word):
    ta_letters = list()
    not_empty = False
    for c in word:
        if c in _GLL:
            ta_letters.append(c)
            not_empty = True
            continue

        if c in accent_symbol_set:
            if not not_empty:
                # odd situation
                ta_letters.append(c)
                not_empty = True
            else:
                ta_letters[-1] += c
            continue

        cval = ord(c)
        if cval < 256 or not (is_tamil_unicode_value(cval)):
            ta_letters.append(c)
            continue

        if not_empty:
            ta_letters[-1] += c
        else:
            ta_letters.append(c)
            not_empty = True

    return ta_letters


_all_symbols = copy(accent_symbols)
_all_symbols.extend(pulli_symbols)
all_symbol_set = _make_set(_all_symbols)


def get_words(letters, tamil_only=False):
    return [word for word in get_words_iterable(letters, tamil_only)]


def get_words_iterable(letters, tamil_only=False):
    # correct algorithm for get-tamil-words
    buf = []
    for idx, let in enumerate(letters):
        if not let.isspace():
            if istamil(let) or (not tamil_only):
                buf.append(let)
        else:
            if len(buf) > 0:
                yield "".join(buf)
                buf = []
    if len(buf) > 0:
        yield "".join(buf)


def cmp(x, y):
    if x == y:
        return 0
    if x > y:
        return 1
    return -1

def unicode_normalize(cplxchar):
    Laa = "ள"
    kaal = "ா"
    sinna_kombu_a = "ெ"
    periya_kombu_aa = "ே"
    sinna_kombu_o = "ொ"
    periya_kombu_oo = "ோ"
    kombu_ak = "ௌ"

    lcplx = len(cplxchar)
    if lcplx >= 3 and cplxchar[-1] == Laa:
        if cplxchar[-2] == sinna_kombu_a:
            return cplxchar[:-2] + kombu_ak
    if lcplx >= 2 and cplxchar[-1] == kaal:
        if cplxchar[-2] == sinna_kombu_a:
            return cplxchar[:-2] + sinna_kombu_o
        if cplxchar[-2] == periya_kombu_aa:
            return cplxchar[:-2] + periya_kombu_oo
    # no-op
    return cplxchar


def splitMeiUyir(uyirmei_char):
    if not isinstance(uyirmei_char, str):
        raise ValueError("Passed input letter '%s' must be unicode, \
                                not just string" % uyirmei_char)

    if (uyirmei_char in mei_letters or uyirmei_char in uyir_letters
            or uyirmei_char in ayudha_letter):
        return uyirmei_char

    if uyirmei_char not in grantha_uyirmei_letters:
        if not is_normalized(uyirmei_char):
            norm_char = unicode_normalize(uyirmei_char)
            rval = splitMeiUyir(norm_char)
            return rval
        raise ValueError("Passed input letter '%s' is not tamil letter" %
                         uyirmei_char)

    idx = grantha_uyirmei_letters.index(uyirmei_char)
    uyiridx = idx % 12
    meiidx = int((idx - uyiridx) / 12)
    return (grantha_mei_letters[meiidx], uyir_letters[uyiridx])
