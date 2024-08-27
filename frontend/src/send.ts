import { StreamSend, StreamingAdapterObserver } from '@nlux/react';


let history = '';

// Function to send query to the server and receive a stream of chunks as response
export const send: StreamSend = async (
    prompt: string,
    observer: StreamingAdapterObserver,
) => {
    
    const response = await fetch('/chat?query=' + encodeURIComponent(prompt) + '&history=' + encodeURIComponent(history), {
        method: 'GET',
    });

    if (response.status !== 200) {
        observer.error(new Error('Failed to connect to the server'));
        return;
    }

    if (!response.body) {
        return;
    }
    history += prompt + '\n';

    // Read a stream of server-sent events
    // and feed them to the observer as they are being generated
    const reader = response.body.getReader();
    const textDecoder = new TextDecoder();

    while (true) {
        const {value, done} = await reader.read();
        if (done) {
            history += '\n';
            break;
        }
        history += value;

        const content = textDecoder.decode(value);
        if (content) {
            observer.next(content);
        }
    }

    observer.complete();
};
