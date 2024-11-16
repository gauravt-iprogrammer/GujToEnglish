from transformers import AutoModelForCTC, Wav2Vec2Processor, Wav2Vec2ProcessorWithLM
import torchaudio
import torch
from deep_translator import GoogleTranslator


# Specify the Hugging Face Model Id 
MODEL_ID = "ai4bharat/indicwav2vec-hindi"

# Specify the Device Id on where to put the model
DEVICE_ID = "cuda" if torch.cuda.is_available() else "cpu"

# Specify Decoder Type:
DECODER_TYPE = "greedy" # Choose "LM" decoding or "greedy" decoding

# Load Model
model_instance = AutoModelForCTC.from_pretrained(MODEL_ID).to(DEVICE_ID)

if DECODER_TYPE == "greedy":
    # Load Processor without language model
    processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)
else:
    # Load Processor with language model
    processor = Wav2Vec2ProcessorWithLM.from_pretrained(MODEL_ID)




def load_audio_from_file(file_path):
    waveform, sample_rate = torchaudio.load(file_path)
    num_channels, _ = waveform.shape
    # if num_channels == 1:
    return waveform[0], sample_rate
    # else:
    #     raise ValueError("Waveform with more than 1 channels are not supported.")
    

def get_transcribe(name):
    TARGET_SAMPLE_RATE = 16000

    #Load from file
    waveform, sample_rate = load_audio_from_file(name)

    #Resample
    resampled_audio = torchaudio.functional.resample(waveform, sample_rate, TARGET_SAMPLE_RATE)


    # Process audio data
    input_tensor = processor(resampled_audio, return_tensors="pt", sampling_rate=TARGET_SAMPLE_RATE).input_values

    # Run forward pass
    with torch.no_grad():
        logits = model_instance(input_tensor.to(DEVICE_ID)).logits.cpu()


    # Decode
    if DECODER_TYPE == "greedy":
        prediction_ids = torch.argmax(logits, dim=-1)
        output_str = processor.batch_decode(prediction_ids)[0]
        translated = GoogleTranslator(source='auto', target='en').translate(output_str)
    # langs_list = GoogleTranslator().get_supported_languages() 
        # print(f"Greedy Decoding: {output_str}")
        print("audio transcribed and translated")
        return {
                "english":translated,
                "gujrati":output_str
                }
    else:
        output_str = processor.batch_decode(logits.numpy()).text[0]
        print(f"LM Decoding: {output_str}")
    

# print(get_transcribe("/home/iproadmin/Downloads/sample.wav"))