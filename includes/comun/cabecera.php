<?php
function mostrarSaludo() {
	if (isset($_SESSION["login"]) && ($_SESSION["login"]===true)) {
		echo "<a href='profile.php'>Profile</a> <a href='logout.php'>Log Out</a>";
		
	} else {
		echo "<a href='login.php'>Log In</a> <a href='registro.php'>Sign Up</a>";
	}
}
?>

<header>
	<div class="title">
		<h1 style="margin-bottom:0;"><a href="index.php">Maude Web Interface</a></h1>
		<p style="margin-top:0; color: #646464; font-size: 13px;text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.1);">An online gateway to The Maude Programming Language</p>
	</div>
	<div class="nav-container">
		<a href="index.php">Home</a>
        <a target="_blank" class="item" href="https://maude.cs.illinois.edu/w/images/e/e9/Maude34manual.pdf">Maude Manual<i class="fas fa-external-link-alt"></i></a>
        <a target="_blank" class="item" href="https://maude.cs.illinois.edu/w/index.php/The_Maude_System">The Maude System<i class="fas fa-external-link-alt"></i></a>
		<a class="item" href="mailto:bcarranc@ucm.es">Contact</a>
		<div class="saludo">
			<?= mostrarSaludo() ?>
		</div>
	</div>
</header>