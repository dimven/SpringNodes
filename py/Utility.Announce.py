import clr
clr.AddReference('System.Speech')
import System.Speech as sp
import System.Speech.Synthesis as sy

se = sy.SpeechSynthesizer()
se.SelectVoiceByHints(sy.VoiceGender.Female, sy.VoiceAge.Adult)
se.Rate = 3
se.SpeakAsync(IN[0])