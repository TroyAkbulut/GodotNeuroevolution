extends Node
class_name UDPManager

@export var platformManager : PlatformManager
@export var playerManager : PlayerManager

const SIGNAL_START : int = 1
const SIGNAL_REQUEST : int = 2
const SIGNAL_DATA : int = 3
const SIGNAL_STOP : int = 4
const SIGNAL_TEST : int = -1

var server : UDPServer
var pythonClient : PacketPeerUDP
var thread : Thread
var running : bool = false

var randomSeed : int = 2158780444

func _ready():
	set_physics_process(false)
	StartServerAndPythonThread()
	
	while pythonClient == null:
		server.poll()
		if server.is_connection_available():
			pythonClient = server.take_connection()
			pythonClient.put_packet("Connected Successfully".to_utf8_buffer())
			
	var recievedPacket = pythonClient.get_packet()
	set_physics_process(true)

func _physics_process(delta):
	server.poll()
	if pythonClient.get_available_packet_count() <= 0:
		return
	
	if not running:
		var data = GetData()
		
		if data.signal == SIGNAL_START:
			seed(randomSeed)
			StartSimulation(data)
			
		if data.signal == SIGNAL_TEST:
			LevelManager.LoadLevel(2)
	
	else:
		var data = GetData()
		if data.signal == SIGNAL_REQUEST:
			ProcessStep(data)

func StartServerAndPythonThread():
	#thread = Thread.new()
	#thread.start(RunPythonProgram)
	server = UDPServer.new()
	server.listen(4242)

func RunPythonProgram():
	OS.execute("python", ["godotUDP.py"])
	
func GetData():
	var packet = pythonClient.get_packet()
	var recievedJson : JSON = JSON.new()
	var error = recievedJson.parse(packet.get_string_from_utf8())
	var recievedData = recievedJson.data
	
	return recievedData
	
func SendData(data):
	var jsonData : String = JSON.stringify(data)
	pythonClient.put_packet(jsonData.to_utf8_buffer())

func StartSimulation(data):
	for playerID in data.data:
		playerManager.SpawnPlayer(playerID)
		
	playerManager.StartPlayers()
	platformManager.Reset()
	running = true
	
func ProcessStep(data):
	var platformData = playerManager.platformManager.GetPlatformDataForPrediction()
		
	var playerInfo = []
	for player in playerManager.players:
		var normalisedPlayerPositions = playerManager.NormalisePlayerCoords(player)
		var playerData	: Dictionary = {
			"playerID": player.playerID,
			"x": normalisedPlayerPositions["x"],
			"y": normalisedPlayerPositions["y"],
			"alive": player.alive,
		}
		playerInfo.append(playerData)
	
	var dataToSend	: Dictionary = {
		"platformData": platformData,
		"playerInfo": playerInfo
	}
	
	if data.signal == SIGNAL_REQUEST:
		SendData(dataToSend)
		
	while pythonClient.get_available_packet_count() <= 0:
		server.poll()
	
	data = GetData()
	if data.signal == SIGNAL_DATA:
		for agentData in data.data:
			playerManager.DoPlayerMove(agentData)
			
	if data.signal == SIGNAL_STOP:
		var playerScores = playerManager.GetScoresAndRemovePlayers()
		platformManager.set_physics_process(false)
		SendData(playerScores)
		running = false
		
