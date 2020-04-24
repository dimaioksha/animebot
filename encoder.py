
from keras.layers import Conv2D, MaxPooling2D, UpSampling2D, Input
from keras.layers import Input, Dense, Flatten, Reshape
from keras.models import Model
from keras.layers import Reshape
from keras import backend as K

#Before prediction


def create_deep_conv_ae():
    input_img = Input(shape=(64, 64, 3))

    x = Conv2D(512, (8, 8), activation='relu', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(64, (2, 2), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    encoded = Conv2D(1, (8, 8), activation='relu', padding='same')(x)
    vector = Flatten()(encoded)
    vector = Dense(256, activation='relu')(vector)
    to_dec = Reshape((16, 16, 1))(vector)
    # vector.reshape(7,7,1)

    input_encoded = Input(shape=(16, 16, 1))

    x = Conv2D(64, (2, 2), activation='relu', padding='same')(input_encoded)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(512, (2, 2), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    decoded = Conv2D(3, (8, 8), activation='sigmoid', padding='same')(x)

    encoder = Model(input_img, to_dec, name="encoder")
    decoder = Model(input_encoded, decoded, name="decoder")
    autoencoder = Model(input_img, decoder(encoder(input_img)), name="autoencoder")
    return encoder, decoder, autoencoder
def getting_encoder():
    encoder, decoder, autoencoder = create_deep_conv_ae()
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
    autoencoder.load_weights("model.h5")
    weights_encoder = autoencoder.layers[1].get_weights()
    encoder.set_weights(weights_encoder)
    return encoder