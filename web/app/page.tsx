"use client";

import WebGPUCanvas from '@/components/Canvas';
import Link from 'next/link';

export default function Home() {
	return (
		<div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-6">
			{/* Side-by-Side Layout */}
			<div className="flex flex-col md:flex-row items-center justify-center gap-8 max-w-6xl w-full">
				{/* Simulation Section */}
				<div className="w-full md:w-1/2">
					<h1 className="text-3xl font-bold text-center md:text-left text-gray-800 mb-2">🧪 Neural Cellular Automata Simulator</h1>
					<p className="text-center md:text-left text-gray-600 mb-4">
						Experience the dynamics of Neural Cellular Automata in real-time.
					</p>
					<WebGPUCanvas />
				</div>

				{/* Main Content */}
				<div className="w-full md:w-1/2 text-center md:text-left space-y-4">
					<h2 className="text-3xl font-bold text-gray-800">Welcome to Neural Cellular Automata</h2>
					<p className="text-gray-600 leading-relaxed">
						We are a research project team under <strong>Monash DeepNeuron</strong>, exploring the potential of Neural Cellular Automata (NCA) for various applications. 
						Our goal is to understand, simulate, and improve NCA models.
					</p>

					{/* Explore Section */}
					<div>
						<h2 className="text-2xl font-semibold text-gray-700">🌐 Explore More:</h2>
						<ul className="space-y-2 mt-2">
							<li>
								<Link href="/nca-intro" className="text-blue-500 hover:underline hover:text-blue-700 transition">
									📘 What is Neural Cellular Automata?
								</Link>
							</li>
							<li>
								<Link href="/nca-research" className="text-blue-500 hover:underline hover:text-blue-700 transition">
									🔬 Our Research & Latest Findings
								</Link>
							</li>
							<li>
								<Link href="/simulator-home" className="text-blue-500 hover:underline hover:text-blue-700 transition">
									🧪 Try the NCA Simulator
								</Link>
							</li>
							<li>
								<Link href="/keeping-up" className="text-blue-500 hover:underline hover:text-blue-700 transition">
									📰 Project Updates
								</Link>
							</li>
						</ul>
					</div>

					{/* Join Us Section */}
					<div className="mt-4">
						<h2 className="text-2xl font-semibold text-gray-700">🤝 Join Us!</h2>
						<p className="text-gray-600 mt-1">
							Interested in working on this project? We'd love to hear from you!
						</p>
						<a
							href="https://www.deepneuron.org/contact-us"
							target="_blank"
							rel="noopener noreferrer"
							className="inline-block bg-blue-600 text-white px-6 py-2 rounded-md mt-3 hover:bg-blue-700 transition"
						>
							Get in Touch
						</a>
					</div>
				</div>
			</div>
		</div>
	);
}
