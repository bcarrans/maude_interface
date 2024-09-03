<?php

require_once __DIR__.'/includes/config.php';

$tituloPagina = 'Contenido';

$contenidoPrincipal = '';

	$contenidoPrincipal .= <<<EOS
	<div class="syntax">
	<p>The Maude commands this platform currently supports are the following:</p>
	<ul>
		<li>Rewriting commands
			<ul>
				<li><code>reduce</code> (may be abbreviated to <code>red</code>)</li>
				<li><code>rewrite</code> (may be abbreviated to <code>rew</code>)</li>
				<li><code>frewrite</code> (may be abbreviated to <code>frew</code>)</li>
				<li><code>erewrite</code> (may be abbreviated to <code>erew</code>)</li>
			</ul>
		</li>
		<li>Matching commands
			<ul>
				<li><code>match</code></li>
				<li><code>xmatch</code></li>
			</ul>
		</li>
		<li>Searching commands
			<ul>
				<li><code>search</code></li>
			</ul>
		</li>
	</ul>

	<p>More information on the Maude system can be found in the following manual:</p>
	<ul>
		<li>Clavel, M., Durán, F., Eker, S., Escobar, S., Lincoln, P., Martí-Oliet, N., Meseguer, J., Rubio, R., & Talcott, C. (2024). <i>Maude Manual, Version 3.4</i>.<br>University of Illinois at Urbana-Champaign. Available at <a href="https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf">https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf</a> <i class="fas fa-external-link-alt" style="font-size: 0.7em;"></i>.</li>
	</ul>

	<p>The syntax to be used is specified in the Appendix A which is available <a href="https://maude.lcc.uma.es/maude-manual/maude-manualap1.html#x129-311000A">here</a> <i class="fas fa-external-link-alt" style="font-size: 0.7em;"></i> in HTML format.</p>
	</div>
	EOS;


require __DIR__.'/includes/plantillas/plantilla.php';